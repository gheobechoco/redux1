from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.auth import HTTPBasicAuth
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from backend.app.core.config import Settings
from backend.app.core.cache import BaseCache


CMR_SEARCH_URL = "/search/granules.umm_json"


class NasaApiError(Exception):
    pass


@dataclass
class NasaClient:
    settings: Settings
    cache: BaseCache

    def _edl_auth(self) -> HTTPBasicAuth:
        if not self.settings.earthdata_username or not self.settings.earthdata_password:
            raise NasaApiError("Missing EARTHDATA_USERNAME or EARTHDATA_PASSWORD in environment")
        return HTTPBasicAuth(self.settings.earthdata_username, self.settings.earthdata_password)

    def _cache_key(self, prefix: str, parts: List[str]) -> str:
        joined = ":".join(parts)
        b64 = base64.urlsafe_b64encode(joined.encode("utf-8")).decode("utf-8").rstrip("=")
        return f"{prefix}:{b64}"

    @retry(reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4), retry=retry_if_exception_type((requests.RequestException,)))
    def search_granules(
        self,
        short_name: str,
        start: str,
        end: str,
        bbox: Optional[Tuple[float, float, float, float]] = None,
        provider: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "short_name": short_name,
            "temporal": f"{start},{end}",
            "page_size": page_size,
            "sort_key": "-start_date",
        }
        if bbox:
            params["bounding_box"] = ",".join(str(x) for x in bbox)
        if provider:
            params["provider_short_name"] = provider

        key = self._cache_key("cmr", [short_name, params["temporal"], params.get("bounding_box", ""), str(page_size)])
        cached = self.cache.get(key)
        if cached:
            return json.loads(cached)

        url = f"{self.settings.cmr_base_url}{CMR_SEARCH_URL}"
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 401:
            # Some CMR endpoints require auth depending on collection; attach EDL
            resp = requests.get(url, params=params, timeout=30, auth=self._edl_auth())
        if not resp.ok:
            raise NasaApiError(f"CMR search failed: {resp.status_code}: {resp.text[:300]}")
        data = resp.json()
        # Basic validation
        if not isinstance(data, dict) or "items" not in data:
            raise NasaApiError("Unexpected CMR response format")

        self.cache.set(key, json.dumps(data), ttl_seconds=3600)
        return data

    @retry(reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4), retry=retry_if_exception_type((requests.RequestException,)))
    def get_power_precip_daily(
        self,
        latitude: float,
        longitude: float,
        start: str,
        end: str,
    ) -> Dict[str, Any]:
        # Use NASA POWER as a pragmatic initial daily precipitation source for basic probability
        base = self.settings.power_base_url
        params = {
            "parameters": "PRECTOTCORR",
            "community": "RE",
            "latitude": latitude,
            "longitude": longitude,
            "start": start,
            "end": end,
            "format": "JSON",
        }
        key = self._cache_key("power", [str(latitude), str(longitude), start, end])
        cached = self.cache.get(key)
        if cached:
            return json.loads(cached)

        resp = requests.get(base, params=params, timeout=30)
        if not resp.ok:
            raise NasaApiError(f"POWER API failed: {resp.status_code}: {resp.text[:300]}")
        data = resp.json()
        # Validate response has the expected structure
        if "properties" not in data or "parameter" not in data["properties"]:
            raise NasaApiError("Unexpected POWER response format")
        self.cache.set(key, json.dumps(data), ttl_seconds=6 * 3600)
        return data

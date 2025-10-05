from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from backend.app.core.config import Settings
from backend.app.core.cache import BaseCache
from backend.app.models.weather_models import (
    PrecipitationProbabilityRequest,
    PrecipitationProbabilityResponse,
    ProbabilityCounts,
    ProbabilityStats,
)
from backend.app.services.nasa_client import NasaClient


@dataclass
class WeatherCalculator:
    settings: Settings
    cache: BaseCache

    def _format_date_range(self, month: int, day: int) -> tuple[str, str]:
        start_year = self.settings.start_year
        end_year = self.settings.end_year
        start = f"{start_year:04d}{month:02d}{day:02d}"
        end = f"{end_year:04d}{month:02d}{day:02d}"
        return start, end

    def _extract_daily_precip(self, power_json: Dict) -> Dict[str, float]:
        parameter = power_json["properties"]["parameter"]["PRECTOTCORR"]
        # parameter is mapping of YYYYMMDD -> value
        # Convert values to float, skip invalid
        result: Dict[str, float] = {}
        for k, v in parameter.items():
            try:
                result[k] = float(v)
            except Exception:
                # skip non-parsable values (e.g., -99 or None)
                continue
        return result

    def _compute_stats(self, values: List[float]) -> Dict[str, float]:
        if not values:
            return {
                "mean": 0.0,
                "median": 0.0,
                "p90": 0.0,
            }
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        mean_v = sum(sorted_vals) / n
        # median
        if n % 2 == 1:
            median_v = sorted_vals[n // 2]
        else:
            median_v = 0.5 * (sorted_vals[n // 2 - 1] + sorted_vals[n // 2])
        # p90 (nearest-rank method)
        rank = max(1, int(round(0.9 * n)))
        p90_v = sorted_vals[min(rank - 1, n - 1)]
        return {"mean": mean_v, "median": median_v, "p90": p90_v}

    def compute_precipitation_probability(
        self, request: PrecipitationProbabilityRequest
    ) -> PrecipitationProbabilityResponse:
        start, end = self._format_date_range(request.month, request.day)

        # Fetch historical daily precip for the same month/day across all years
        power = NasaClient(settings=self.settings, cache=self.cache)
        data = power.get_power_precip_daily(
            latitude=request.latitude, longitude=request.longitude, start=start, end=end
        )
        series = self._extract_daily_precip(data)

        # Filter to exactly the day-of-year across years (handle leap year Feb 29 gracefully)
        target_month = request.month
        target_day = request.day
        selected_values: List[float] = []
        for date_str, val in series.items():
            # date_str like YYYYMMDD
            try:
                m = int(date_str[4:6])
                d = int(date_str[6:8])
            except Exception:
                continue
            if m == target_month and d == target_day:
                selected_values.append(val)
            elif target_month == 2 and target_day == 29 and m == 2 and d in (28, 29):
                selected_values.append(val)

        total_days = len(selected_values)
        missing_days = 0  # we skip invalid entries during parsing

        rainy_days = sum(1 for v in selected_values if v >= request.threshold_mm)
        heavy_rain_days = sum(1 for v in selected_values if v >= 20.0)

        rain_prob = float(100.0 * rainy_days / total_days) if total_days else 0.0
        heavy_prob = float(100.0 * heavy_rain_days / total_days) if total_days else 0.0

        stats = self._compute_stats(selected_values)
        mean_precip = float(stats["mean"]) if total_days else 0.0
        median_precip = float(stats["median"]) if total_days else 0.0
        p90_precip = float(stats["p90"]) if total_days else 0.0

        return PrecipitationProbabilityResponse(
            query=request,
            rain_probability=round(rain_prob, 2),
            heavy_rain_probability=round(heavy_prob, 2),
            counts=ProbabilityCounts(
                all_days=int(total_days),
                rainy_days=rainy_days,
                heavy_rain_days=heavy_rain_days,
                missing_days=missing_days,
            ),
            stats=ProbabilityStats(
                mean_precip_mm=round(mean_precip, 3),
                median_precip_mm=round(median_precip, 3),
                percentile_90_precip_mm=round(p90_precip, 3),
            ),
            meta={
                "source": "NASA POWER daily PRECTOTCORR",
                "method": "historical_frequency_analysis",
                "units": "mm/day",
                "period": f"{self.settings.start_year}-{self.settings.end_year}",
            },
        )

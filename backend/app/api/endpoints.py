from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.app.api.dependencies import get_calculator, get_nasa_client
from backend.app.models.weather_models import (
    PrecipitationProbabilityRequest,
    PrecipitationProbabilityResponse,
)
from backend.app.services.calculator import WeatherCalculator
from backend.app.services.nasa_client import NasaClient


router = APIRouter()


@router.get("/probability/precipitation", response_model=PrecipitationProbabilityResponse)
async def get_precipitation_probability(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    month: int = Query(..., ge=1, le=12),
    day: int = Query(..., ge=1, le=31),
    threshold_mm: float = Query(1.0, ge=0),
    calculator: WeatherCalculator = Depends(get_calculator),
) -> PrecipitationProbabilityResponse:
    request = PrecipitationProbabilityRequest(
        latitude=lat, longitude=lon, month=month, day=day, threshold_mm=threshold_mm
    )
    return calculator.compute_precipitation_probability(request)


@router.get("/nasa/cmr/granules")
async def cmr_search_granules(
    short_name: str = Query("GPM_3IMERGDF"),
    start: str = Query(..., description="ISO start datetime, e.g., 2019-06-15T00:00:00Z"),
    end: str = Query(..., description="ISO end datetime, e.g., 2019-06-16T00:00:00Z"),
    bbox: Optional[str] = Query(
        None, description="Comma-separated lonW,latS,lonE,latN bounding box"
    ),
    nasa: NasaClient = Depends(get_nasa_client),
):
    bbox_tuple = None
    if bbox:
        parts = [p.strip() for p in bbox.split(",")]
        if len(parts) == 4:
            bbox_tuple = (float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]))
    result = nasa.search_granules(short_name=short_name, start=start, end=end, bbox=bbox_tuple)
    return result

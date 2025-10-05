from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class PrecipitationProbabilityRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    threshold_mm: float = Field(1.0, ge=0)


class ProbabilityCounts(BaseModel):
    all_days: int
    rainy_days: int
    heavy_rain_days: int
    missing_days: int


class ProbabilityStats(BaseModel):
    mean_precip_mm: float
    median_precip_mm: float
    percentile_90_precip_mm: float


class PrecipitationProbabilityResponse(BaseModel):
    query: PrecipitationProbabilityRequest
    rain_probability: float = Field(..., ge=0, le=100)
    heavy_rain_probability: float = Field(..., ge=0, le=100)
    counts: ProbabilityCounts
    stats: ProbabilityStats
    meta: dict[str, Optional[str]] = {}

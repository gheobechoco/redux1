from __future__ import annotations

from pydantic import BaseModel, Field


class ProbabilityResult(BaseModel):
    probability: float = Field(..., ge=0, le=100)
    total: int
    count: int

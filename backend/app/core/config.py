from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()  # Load variables from a local .env if present


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Will It Rain On My Parade API")
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")

    # Redis
    redis_url: str | None = os.getenv("REDIS_URL")

    # NASA Earthdata / EDL
    earthdata_username: str | None = os.getenv("EARTHDATA_USERNAME")
    earthdata_password: str | None = os.getenv("EARTHDATA_PASSWORD")
    cmr_base_url: str = os.getenv("CMR_BASE_URL", "https://cmr.earthdata.nasa.gov")
    ges_disc_base_url: str = os.getenv("GES_DISC_BASE_URL", "https://disc.gsfc.nasa.gov")

    # POWER API (initial data source for precipitation timeseries)
    power_base_url: str = os.getenv(
        "POWER_BASE_URL", "https://power.larc.nasa.gov/api/temporal/daily/point"
    )

    # Data defaults
    start_year: int = int(os.getenv("START_YEAR", "2000"))
    end_year: int = int(os.getenv("END_YEAR", "2023"))


settings = Settings()

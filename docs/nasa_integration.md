# NASA Integration Details

## Earthdata Login (EDL)
- Provide `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` via environment.
- Some endpoints require authentication, others are public. The client retries with EDL auth on 401.

## CMR (Common Metadata Repository)
- Base: `https://cmr.earthdata.nasa.gov`
- Granule search endpoint used: `/search/granules.umm_json`
- Parameters: `short_name`, `temporal`, optional `bounding_box`, `page_size`, `sort_key`.

## POWER API
- Endpoint: `https://power.larc.nasa.gov/api/temporal/daily/point`
- Parameter `PRECTOTCORR` provides corrected precipitation (mm/day)
- We request the range from START_YEAR to END_YEAR for a given month-day pair.
- Response is validated to contain `properties.parameter.PRECTOTCORR`.

## Validation and Error Handling
- Network errors and 5xxs: retried with exponential backoff (max 3 attempts)
- 401 on CMR: retried once with EDL auth
- Response schemas are sanity-checked; unexpected formats raise `NasaApiError`
- Results cached (Redis if configured, fallback to in-memory)

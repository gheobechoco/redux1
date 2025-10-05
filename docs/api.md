# API Documentation (Phase 1)

## Health
GET `/health`
- 200: `{ "status": "ok" }`

## Precipitation Probability
GET `/api/probability/precipitation`

### Query Parameters
- `lat` (float, required, -90..90)
- `lon` (float, required, -180..180)
- `month` (int, 1..12)
- `day` (int, 1..31)
- `threshold_mm` (float, default 1.0)

### Response
```
{
  "query": { ... },
  "rain_probability": 42.1,
  "heavy_rain_probability": 3.2,
  "counts": { "all_days": 23, "rainy_days": 8, "heavy_rain_days": 1, "missing_days": 0 },
  "stats": { "mean_precip_mm": 1.23, "median_precip_mm": 0.4, "percentile_90_precip_mm": 3.3 },
  "meta": { "source": "NASA POWER daily PRECTOTCORR", "method": "historical_frequency_analysis", "units": "mm/day", "period": "2000-2023" }
}
```

## CMR Granule Search
GET `/api/nasa/cmr/granules`

### Query Parameters
- `short_name` (string, default `GPM_3IMERGDF`)
- `start` (ISO datetime)
- `end` (ISO datetime)
- `bbox` (string, optional, `lonW,latS,lonE,latN`)

### Response
- Pass-through of CMR UMM-JSON result with minimal validation.

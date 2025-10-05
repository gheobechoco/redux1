# Setup Instructions

These steps get you running the backend and frontend for the "Will It Rain On My Parade?" project.

## Prerequisites
- Python 3.11+
- Node.js 18+
- (Optional) Redis server if you want persistent caching
- NASA Earthdata Login credentials: create an account and generate an application password if using 2FA.

## Configuration
1. Copy `config/.env.template` to `.env` at the repository root:

```bash
cp config/.env.template .env
```

2. Fill in your NASA EDL credentials in `.env`:
```
EARTHDATA_USERNAME=your_username
EARTHDATA_PASSWORD=your_password
```

3. (Optional) Set `REDIS_URL` if you run Redis. Otherwise, in‑memory cache will be used.

## Backend
1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Run the API:
```bash
uvicorn backend.main:app --reload --port 8000
```

4. Test health endpoint:
```bash
curl http://localhost:8000/health
```

5. Test precipitation probability endpoint:
```bash
curl "http://localhost:8000/api/probability/precipitation?lat=48.8566&lon=2.3522&month=6&day=15&threshold_mm=1"
```

## Frontend
A starter React app is included or will be scaffolded under `frontend/`.

- Development server (after dependencies install):
```bash
npm --prefix frontend install
npm --prefix frontend run dev
```

## Notes on NASA APIs
- CMR search supports unauthenticated access for most collections; some require EDL auth.
- For Phase 1 probability we pragmatically use NASA POWER daily precipitation (PRECTOTCORR) for 2000‑2023, which is suitable for climatology summaries. GPM IMERG integration will be added next.
- Keep responses under 5 seconds by caching and minimizing network round‑trips.

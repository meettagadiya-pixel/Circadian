# Circadian Intelligence Platform

A real-time physiological intelligence system that analyses wearable biometric data to detect circadian misalignment and deliver personalised behavioural interventions (zeitgebers).

Built by Meet Tagadiya for Andrea's Loop Orchestra integration.

---

## What This System Does

The platform collects data from wearables (Fitbit, Oura) and a continuous glucose monitor (Freestyle Libre) via the Junction API, analyses the user's biological clock against their social/behavioural clock, and generates personalised time-giver recommendations to reduce circadian disruption.

**Three layers:**
1. **Data Ingestion** — Junction API fetches HRV, heart rate, steps, sleep, glucose, and CBT every minute
2. **Digital Twin** — pipeline computes biological midnight from CBT nadir, misalignment score, fatigue, readiness, and Circadian Stress Index
3. **Intervention Engine** — rule-based zeitgeber generator that produces personalised messages using real values (actual times, real scores, not generic text)

---

## Project Structure

```
Circadian/
├── backend/                        # FastAPI backend
│   ├── main.py                     # App entry point, router registration
│   ├── workers/
│   │   └── physiology_worker.py    # Core pipeline — runs every minute
│   ├── app/
│   │   ├── analytics/
│   │   │   ├── digital_twin_engine.py    # Biological midnight, DLMO, misalignment
│   │   │   ├── risk_engine.py            # Circadian Stress Index (0-100)
│   │   │   └── adherence_engine.py       # Behavioural adherence scoring
│   │   ├── interventions/
│   │   │   ├── circadian_interventions.py  # Zeitgeber generation
│   │   │   └── contextual_engine.py        # Meal/exercise timing analysis
│   │   ├── api/
│   │   │   ├── dashboard_summary.py  # Main frontend API endpoint
│   │   │   ├── readiness_score.py    # HRV-based readiness (evidence-based weights)
│   │   │   ├── behavior_logger.py    # Meal/exercise/sleep logging
│   │   │   └── ...
│   │   ├── ingestion/
│   │   │   └── junction_fetcher.py   # Junction API calls
│   │   └── environment/
│   │       └── light_cycle.py        # OpenWeather — reads lat/lon from user_locations table
│   ├── saved_models/               # Not used — ML model replaced with transparent formula
│   ├── requirements.txt
│   └── .env                        # Secret credentials — never commit this
│
└── circadian-v2/                   # Nuxt.js frontend
    ├── pages/circadian/
    │   ├── index.vue               # Dashboard
    │   ├── timeline.vue            # 24h biological clock view
    │   ├── interventions.vue       # Zeitgebers + behavioral logging
    │   └── trends.vue              # Longitudinal analysis
    ├── layouts/default.vue         # Sidebar + topbar layout
    ├── plugins/user-store.js       # User state management
    └── nuxt.config.js
```

---

## Local Setup — Backend

### Requirements
- Python 3.10+
- pip

### Install

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
# Junction API (wearable data)
VITAL_BASE_URL=https://api.sandbox.eu.junction.com   # sandbox
# VITAL_BASE_URL=https://api.eu.junction.com         # production (real users)
VITAL_API_KEY=your_junction_api_key

# OpenWeather (environmental context)
OPENWEATHER_API_KEY=your_openweather_key

# Supabase (database)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_publishable_key

# CORS — set to your frontend domain in production
FRONTEND_URL=http://localhost:3000
```

### Run

```bash
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`

Health check: `http://localhost:8000/health` — shows pipeline status and last run time.

API docs: `http://localhost:8000/docs`

---

## Local Setup — Frontend

### Requirements
- Node.js 16+

### Install

```bash
cd circadian-v2
npm install
```

### Environment Variables

Create `.env` in the `circadian-v2` folder:

```env
CIRCADIAN_API_URL=http://localhost:8000
```

### Run

```bash
npm run dev
```

Frontend runs on `http://localhost:3000`

---

## Supabase Database

### Tables

| Table | Purpose |
|---|---|
| `users` | One row per user. Columns: `id`, `vital_user_id`, `chronotype`, `created_at` |
| `user_provider_connections` | Maps app user to Junction provider. Columns: `user_id`, `provider`, `provider_user_id` |
| `user_locations` | Per-user lat/lon for weather API. Columns: `user_id`, `latitude`, `longitude` |
| `physiological_data` | HRV, CBT, resting heart rate timeseries from wearables |
| `digital_twin_snapshots` | Pipeline output — one snapshot per run per user. Auto-cleaned to last 48 |
| `behavioral_logs` | User-logged meals, exercise, sleep onset |
| `biochemical_data` | Glucose data storage |
| `notification_delivery_log` | Tracks which notifications were already sent |

### Adding a New User (manual process — see Auth section below)

```sql
-- 1. Insert user row
INSERT INTO users (id, vital_user_id, chronotype)
VALUES ('your-uuid', 'junction-provider-user-id', 'intermediate');

-- 2. Insert provider connection
INSERT INTO user_provider_connections (user_id, provider, provider_user_id)
VALUES ('your-uuid', 'junction', 'junction-provider-user-id');

-- 3. Insert location (for weather)
INSERT INTO user_locations (user_id, latitude, longitude)
VALUES ('your-uuid', 45.4064, 11.8768);
```

---

## How the Pipeline Works

The physiology pipeline runs automatically every minute via APScheduler:

```
1. Read all users from Supabase users table
2. For each user:
   a. Fetch activity + sleep summary from Junction
   b. Fetch HRV, heart rate, steps, glucose timeseries from Junction
   c. Read physiological_data rows to compute biological midnight (CBT nadir)
   d. Compute DLMO estimate (biological_midnight - 2h)
   e. Calculate misalignment score (biological vs social clock)
   f. Compute fatigue from HRV (transparent formula, no ML)
   g. Calculate Circadian Stress Index
   h. Calculate readiness score (evidence-based weights)
   i. Generate personalised zeitgeber interventions
   j. Read behavioral_logs for meal/exercise timing analysis
   k. Fetch weather for user's location
   l. Save digital_twin_snapshot to Supabase
3. Auto-cleanup: keep only last 48 snapshots per user
```

The frontend reads only from `digital_twin_snapshots` via the `/dashboard-summary` API — it never calls Junction directly.

---

## Switching from Sandbox to Production

Change one line in `.env`:

```env
# Sandbox (synthetic data, for development):
VITAL_BASE_URL=https://api.sandbox.eu.junction.com

# Production (real user wearables):
VITAL_BASE_URL=https://api.eu.junction.com
```

Everything else stays identical.

---

## Scores — What They Mean and How They're Calculated

### Biological Midnight
Computed from the CBT (core body temperature) nadir in `physiological_data`. The lowest smoothed temperature point minus 2 hours. Source: published circadian physiology.

### DLMO Estimate
Dim Light Melatonin Onset ≈ biological_midnight - 2h. Standard clinical approximation (Lewy et al., 1999). Labelled "estimated" in the UI.

### Misalignment Score (hours)
Gap between biological sleep midpoint and actual sleep time from behavioral logs. When behavioral logs are empty, falls back to a variability proxy from sleep consistency.

### Circadian Stress Index (0-100)
Replaces "Risk Score". Weighted composite:
- Misalignment: 50% (Roenneberg et al., 2012)
- HRV-derived fatigue: 30% (Firstbeat Technologies, 2014)
- Glucose variability: 20% (Scheer et al., 2009)

### Readiness Score (0-100)
- HRV: 55% (Oura validation study, Koskimäki et al., 2018)
- Sleep quality (consistency + fatigue): 28% (Phillips et al., 2017)
- Behavioural adherence: 17% (Baron & Reid, 2014)

### Fatigue Prediction (1-5)
Transparent HRV-based formula — no ML model:
- HRV > 50ms = fatigue 1 (low)
- HRV 35-50ms = fatigue 2
- HRV 20-35ms = fatigue 3
- HRV 10-20ms = fatigue 4
- HRV < 10ms = fatigue 5
- +1 if misalignment > 3h
- +1 if sleep consistency < 40%

---

## What Luigi Needs to Build for Production

### 1. Authentication (Required — high priority)
The API is currently open. Any request with a valid `user_id` returns that user's health data.

**Recommended approach:** Supabase Auth
- Add Supabase Auth to the frontend (email/password or OAuth)
- Frontend sends JWT token with every API request
- Add FastAPI middleware to verify JWT on every endpoint
- Replace hardcoded `user_id` in frontend with the authenticated user's ID from the token

Supabase Auth is already available in the Supabase project — no new service needed.

### 2. User Onboarding Flow (Required for real users)
Currently users are added manually via SQL. For real users:

1. User signs up → Supabase Auth creates account
2. Backend creates a Junction user via `POST /v2/user`
3. Frontend redirects user to Junction Link flow to connect their wearable
4. Junction sends a webhook to `/junction-webhook` when connection succeeds
5. Backend stores `provider_user_id` in `user_provider_connections`
6. Pipeline automatically picks up new user on next run

The webhook endpoint (`/junction-webhook`) already exists. Steps 2-3 need a frontend onboarding screen.

### 3. Location Collection
When a new user registers, collect their location (or use browser geolocation API) and save to `user_locations` table. The weather/light cycle data is per-user and already reads from this table.

### 4. Pipeline as Standalone Worker (Recommended for production)
Currently the pipeline runs inside the FastAPI app. For production stability, separate it:

```bash
# Run pipeline independently
python workers/physiology_worker.py
```

Or use a cron job / Celery worker. This way the pipeline keeps running even if the API restarts.

### 5. CORS Configuration
Set `FRONTEND_URL` in `.env` to Loop Orchestra's domain:

```env
FRONTEND_URL=https://looportchestra.com
```

---

## API Endpoints Used by Frontend

| Endpoint | Method | Description |
|---|---|---|
| `/dashboard-summary?user_id=` | GET | Main data endpoint — returns all dashboard data |
| `/log-behavior` | POST | Log meal, exercise, or sleep event |
| `/behavior-logs?user_id=` | GET | Recent behavioral logs |
| `/health` | GET | Pipeline health status |

All other endpoints exist for debugging and internal use.

---

## Known Limitations (V1)

| Limitation | Notes |
|---|---|
| No authentication | See Luigi's tasks above |
| No user onboarding UI | Users added manually via SQL |
| Environmental light is from OpenWeather | Not from phone sensor — good proxy but not direct measurement |
| DLMO is estimated, not measured | Clinical approximation, labelled "est." in UI |
| Behavioral logs require manual input | No automatic detection of meals/exercise |
| Sandbox data is synthetic | Junction sandbox generates the same dataset for all demo users |
| No error alerting | Check `/health` endpoint; pipeline logs to stdout |

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.10, FastAPI, APScheduler |
| Database | Supabase (PostgreSQL) |
| Wearable data | Junction API (Vital) |
| Glucose data | Freestyle Libre via Junction |
| Weather | OpenWeather API |
| Frontend | Nuxt.js 2, Tailwind CSS |
| Deployment | Any Python host (Railway, Render, Heroku) + Vercel/Netlify for frontend |

---

## Contact

Built by Meet Tagadiya — University of Padua  
For integration questions: hand off to Luigi with this README and the `.env` values separately (never in the repo).

# Circadian Intelligence Platform

A real-time physiological intelligence system that analyses wearable biometric data to detect circadian misalignment and deliver personalised behavioural interventions (zeitgebers).

Built by Meet Tagadiya for Loop Orchestra.

---

## How It Works

Every minute, a background pipeline (`workers/physiology_worker.py`):

1. **Fetches data** from Junction API — HRV, heart rate, steps, sleep, glucose (CGM), and core body temperature from connected wearables (Fitbit, Oura, Freestyle Libre)
2. **Computes the digital twin** — biological midnight (from CBT nadir), DLMO estimate, misalignment score, fatigue, Circadian Stress Index, and readiness score
3. **Generates interventions** — personalised zeitgeber recommendations using real numbers (actual times, actual scores), not generic text
4. **Reads behavioral logs** — meals, exercise, and sleep events logged by the user, to make interventions specific
5. **Fetches weather** for the user's location to assess natural light exposure
6. **Saves a snapshot** to the database, auto-cleaned to the last 48 entries per user

The frontend reads only from these saved snapshots via one endpoint — it never calls Junction directly.

---

## Scores — What They Mean

**Biological Midnight** — computed from real core body temperature data (CBT nadir), not estimated.

**DLMO Estimate** — biological_midnight minus 2 hours. Standard clinical approximation (Lewy et al., 1999). Labelled "estimated" in the UI.

**Misalignment Score** — gap in hours between biological sleep time and actual logged sleep time.

**Fatigue (1–5)** — transparent HRV-based formula, no ML model. Higher HRV = lower fatigue, with modifiers for misalignment and sleep consistency.

**Circadian Stress Index (0–100)** — misalignment 50% + fatigue 30% + glucose variability 20%, weights based on published circadian research (Roenneberg 2012, Firstbeat 2014, Scheer 2009).

**Readiness Score (0–100)** — HRV 55% + sleep quality 28% + adherence 17%, based on Oura's validation methodology and published sleep research.

---

## Project Structure

```
backend/
├── main.py                      # FastAPI app, routers, scheduler startup
├── workers/physiology_worker.py # Core pipeline — runs every 1 minute
├── app/
│   ├── analytics/                # Scoring engines (digital twin, risk, adherence)
│   ├── interventions/            # Zeitgeber generation logic
│   ├── ingestion/                # Junction API calls
│   ├── physiology/                # Biological clock calculations
│   ├── environment/               # Weather + light exposure
│   ├── behaviour/                  # Meal/exercise timing analysis
│   ├── api/                        # All HTTP endpoints
│   └── database/supabase_client.py
├── .env                          # Credentials — sent separately, never in git
└── requirements.txt

circadian-v2/                     # Nuxt.js frontend
├── pages/circadian/
│   ├── index.vue                 # Dashboard
│   ├── timeline.vue               # 24h biological clock, DLMO, CBT
│   ├── interventions.vue          # Zeitgebers + activity logging
│   └── trends.vue                 # Longitudinal trends
├── layouts/default.vue
└── nuxt.config.js
```

---

## Running Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
```

You'll receive a `.env` file separately with the working credentials — place it in the `backend` folder. Then:

```bash
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`. Check `/health` for pipeline status.

### Frontend

```bash
cd circadian-v2
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`. Set `CIRCADIAN_API_URL` in `circadian-v2/.env` to point at the backend.

---

## Switching from Sandbox to Real Wearable Data

One line in `.env`:

```env
# Sandbox (synthetic test data):
VITAL_BASE_URL=https://api.sandbox.eu.junction.com

# Production (real connected wearables):
VITAL_BASE_URL=https://api.eu.junction.com
```

Everything else in the codebase stays identical.

---

## What Still Needs to Be Built

**Authentication** — the API currently has no login system; any request with a `user_id` returns that user's data. Recommended approach: Supabase Auth, with a JWT sent on every request and verified by FastAPI middleware.

**User onboarding** — users are currently added manually in the database. For real users, build a signup flow that creates a Junction user and walks them through connecting their wearable (Junction's hosted Link flow). The webhook endpoint that receives the connection confirmation already exists and works (`/junction-webhook`) — only the frontend onboarding screens are missing.

**CORS** — set `FRONTEND_URL` in `.env` to the production frontend domain.

**Pipeline as standalone process** — currently the pipeline runs inside the FastAPI app via APScheduler. For production stability it's better run as a separate worker process so it survives API restarts.

---

## Known Limitations

- Environmental light is estimated from weather data (OpenWeather), not measured from a phone sensor
- DLMO is a clinical approximation, not directly measured
- Behavioral logging is manual — no automatic detection of meals or exercise
- Sandbox wearable data is synthetic and similar across demo users; real connected devices will produce more varied results

---

## Tech Stack

Python 3.10 / FastAPI / APScheduler · Supabase (PostgreSQL) · Junction API (Fitbit, Oura, Freestyle Libre) · OpenWeather · Nuxt.js 2 / Tailwind CSS

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.ingestion.vital_service import test_vital_connection
from app.environment.light_cycle import fetch_light_cycle
from app.services.scheduler import start_scheduler

# ── Routers ───────────────────────────────────────────────
from app.api.database_test import router as db_router
from app.api.schema_inspector import router as schema_router
from app.api.digital_twin import router as digital_twin_router
from app.api.digital_twin_debug import router as digital_twin_debug_router
from app.api.features import router as features_router
from app.api.labels import router as labels_router
from app.api.ml_prediction import router as ml_router
from app.api.feedback import router as feedback_router
from app.api.intervention_feedback import router as intervention_feedback_router
from app.api.personalization import router as personalization_router
from app.api.trends import router as trends_router
from app.api.snapshots import router as snapshots_router
from app.api.anomalies import router as anomalies_router
from app.api.risk import router as risk_router
from app.api.timeline import router as timeline_router
from app.api.forecast import router as forecast_router
from app.api.monitoring import router as monitoring_router
from app.api.notifications import router as notifications_router
from app.api.junction_summary import router as junction_summary_router
from app.api.demo_provider import router as demo_router
from app.api.junction import router as junction_router
from app.api.vital import router as vital_router
from app.api.junction_sleep import router as junction_sleep_router
from app.api.circadian_analysis import router as circadian_router
from app.api.behavior_logger import router as behavior_router
from app.api.junction_webhook import router as webhook_router
from app.api.due_interventions import router as due_interventions_router
from app.api.notification_preview import router as notification_router
from app.api.notification_delivery import router as notification_delivery_router
from app.api.notification_dispatch import router as notification_dispatch_router
from app.api.notification_history import router as notification_history_router
from app.api.user_dashboard import router as user_dashboard_router
from app.api.dashboard_summary import router as dashboard_summary_router
from app.api.circadian_timeline import router as circadian_timeline_router
from app.api.behavior_timeline import router as behavior_timeline_router
from app.api.combined_timeline import router as combined_timeline_router
from app.api.adherence_summary import router as adherence_summary_router
from app.api.readiness_score import router as readiness_score_router
from app.api.daily_insight import router as daily_insight_router
from app.api.coach_recommendation import router as coach_recommendation_router
from app.api.glucose_log import router as glucose_log_router
from app.api.light_exposure_log import router as light_exposure_log_router
from app.api.light_exposure_summary import router as light_exposure_summary_router
from app.api.cgm_sync import router as cgm_sync_router
from app.api.cgm_summary import router as cgm_summary_router
from app.api.environment_context import router as environment_context_router
from app.api.junction_debug import router as junction_debug_router
from app.api.libre_debug import router as libre_debug_router
from app.api.user_location import router as user_location_router

# ── App ───────────────────────────────────────────────────
app = FastAPI(
    title="Circadian AI Platform",
    description="Backend for circadian digital twin and intervention engine",
    version="0.1.0",
)

# ── CORS ──────────────────────────────────────────────────
# Add Luigi's Loop Orchestra domain here when deploying
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    os.getenv("FRONTEND_URL", ""),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o for o in ALLOWED_ORIGINS if o],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Scheduler — start only in the main worker process ─────
# Prevents double-start when uvicorn --reload spawns a reloader
# process alongside the actual worker process.
@app.on_event("startup")
async def startup_event():
    if os.environ.get("IS_RELOADER") != "true":
        start_scheduler()


# ── Routers ───────────────────────────────────────────────
app.include_router(db_router)
app.include_router(schema_router)
app.include_router(digital_twin_router)
app.include_router(digital_twin_debug_router)
app.include_router(features_router)
app.include_router(labels_router)
app.include_router(ml_router)
app.include_router(feedback_router)
app.include_router(intervention_feedback_router)
app.include_router(trends_router)
app.include_router(personalization_router)
app.include_router(snapshots_router)
app.include_router(anomalies_router)
app.include_router(risk_router)
app.include_router(timeline_router)
app.include_router(forecast_router)
app.include_router(monitoring_router)
app.include_router(notifications_router)
app.include_router(vital_router)
app.include_router(junction_router)
app.include_router(demo_router)
app.include_router(junction_summary_router)
app.include_router(junction_sleep_router)
app.include_router(circadian_router)
app.include_router(behavior_router)
app.include_router(webhook_router)
app.include_router(due_interventions_router)
app.include_router(notification_router)
app.include_router(notification_delivery_router)
app.include_router(notification_dispatch_router)
app.include_router(notification_history_router)
app.include_router(user_dashboard_router)
app.include_router(dashboard_summary_router)
app.include_router(circadian_timeline_router)
app.include_router(behavior_timeline_router)
app.include_router(combined_timeline_router)
app.include_router(adherence_summary_router)
app.include_router(readiness_score_router)
app.include_router(daily_insight_router)
app.include_router(coach_recommendation_router)
app.include_router(glucose_log_router)
app.include_router(light_exposure_log_router)
app.include_router(light_exposure_summary_router)
app.include_router(cgm_sync_router)
app.include_router(cgm_summary_router)
app.include_router(environment_context_router)
app.include_router(junction_debug_router)
app.include_router(libre_debug_router)
app.include_router(user_location_router)


# ── Utility endpoints ─────────────────────────────────────
@app.get("/light-cycle")
def light_cycle():
    return fetch_light_cycle()


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Circadian AI Platform backend is live"
    }


# Track last pipeline run in memory for health check
pipeline_status = {
    "last_run": None,
    "last_status": "not_started",
    "runs_today": 0
}


@app.get("/health")
def health_check():
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    return {
        "status": "healthy",
        "time": now,
        "pipeline": pipeline_status
    }


@app.post("/internal/pipeline-heartbeat")
def pipeline_heartbeat(payload: dict):
    """Called by physiology_worker after each run to update status."""
    pipeline_status["last_run"] = payload.get("timestamp")
    pipeline_status["last_status"] = payload.get("status", "unknown")
    pipeline_status["runs_today"] = payload.get("runs_today", 0)
    return {"ok": True}


@app.get("/config-check")
def config_check():
    return {
        "vital_configured": bool(settings.VITAL_API_KEY),
        "weather_configured": bool(settings.WEATHER_API_KEY),
        "supabase_configured": bool(
            settings.SUPABASE_URL and settings.SUPABASE_KEY
        )
    }


@app.get("/test-vital")
def vital_test():
    return test_vital_connection()
from fastapi import APIRouter

from app.database.supabase_client import supabase

from app.analytics.anomaly_engine import (
    detect_physiological_anomalies
)

router = APIRouter()


@router.get("/anomalies/{user_id}")
def get_anomalies(user_id: str):

    response = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=False)
        .limit(30)
        .execute()
    )

    anomaly_analysis = (
        detect_physiological_anomalies(
            response.data
        )
    )

    return {
        "user_id": user_id,
        "anomaly_analysis": anomaly_analysis
    }
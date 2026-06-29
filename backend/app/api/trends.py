from fastapi import APIRouter

from app.database.supabase_client import supabase
from app.analytics.trend_engine import analyze_snapshot_trends

router = APIRouter()


@router.get("/trends/{user_id}")
def get_trends(user_id: str):
    snapshot_resp = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at")
        .execute()
    )

    trends = analyze_snapshot_trends(
        snapshot_resp.data
    )

    return {
        "user_id": user_id,
        "trends": trends
    }
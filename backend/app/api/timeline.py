from fastapi import APIRouter

from app.database.supabase_client import supabase

from app.analytics.timeline_engine import (
    build_health_timeline
)

router = APIRouter()


@router.get("/timeline/{user_id}")
def get_timeline(user_id: str):

    response = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=False)
        .limit(50)
        .execute()
    )

    timeline = build_health_timeline(
        response.data
    )

    return {
        "user_id": user_id,
        "timeline_points": len(
            timeline
        ),
        "timeline": timeline
    }
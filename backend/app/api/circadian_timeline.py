from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


@router.get("/circadian-timeline")
def circadian_timeline(
    user_id: str
):

    response = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:

        return {
            "status": "no_data",
            "user_id": user_id,
            "timeline": []
        }

    snapshot = response.data[0]

    data = snapshot.get(
        "snapshot_data",
        {}
    )

    circadian_analysis = data.get(
        "circadian_analysis",
        []
    )

    timeline = []

    for item in circadian_analysis:

        timeline.append({

            "sleep_midpoint":
                item.get("sleep_midpoint"),

            "sleep_hours":
                item.get("sleep_hours"),

            "efficiency":
                item.get("efficiency"),

            "hrv":
                item.get("hrv"),

            "recovery_score":
                item.get("recovery_score"),

            "circadian_alignment":
                item.get("circadian_alignment")
        })

    return {
        "status": "success",
        "user_id": user_id,
        "count": len(timeline),
        "timeline": timeline
    }
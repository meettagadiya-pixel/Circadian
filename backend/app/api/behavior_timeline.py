from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


@router.get("/behavior-timeline")
def behavior_timeline(
    user_id: str
):

    response = (
        supabase
        .table("behavioral_logs")
        .select("*")
        .eq("user_id", user_id)
        .order("timestamp", desc=True)
        .limit(100)
        .execute()
    )

    logs = response.data or []

    timeline = []

    for item in logs:

        timeline.append({

            "timestamp":
                item.get(
                    "timestamp"
                ),

            "event_type":
                item.get(
                    "event_type"
                ),

            "notes":
                item.get(
                    "notes"
                )
        })

    return {

        "status":
            "success",

        "user_id":
            user_id,

        "count":
            len(
                timeline
            ),

        "timeline":
            timeline
    }
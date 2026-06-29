from fastapi import APIRouter

from app.database.supabase_client import supabase

from app.analytics.timeline_engine import (
    build_health_timeline
)

from app.analytics.forecast_engine import (
    forecast_risk_direction
)

from app.analytics.notification_engine import (
    generate_notification_strategy
)

router = APIRouter()


@router.get("/notifications/{user_id}")
def get_notification_strategy(
    user_id: str
):

    response = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=False)
        .limit(50)
        .execute()
    )

    snapshots = response.data

    timeline = (
        build_health_timeline(
            snapshots
        )
    )

    forecast = (
        forecast_risk_direction(
            timeline
        )
    )

    latest = snapshots[-1]

    risk_analysis = (
        latest["snapshot_data"]
        .get("risk_analysis", {})
    )

    notification = (
        generate_notification_strategy(
            risk_state=risk_analysis.get(
                "risk_state",
                "low"
            ),

            forecast_direction=forecast.get(
                "risk_direction",
                "stable"
            )
        )
    )

    return {
        "user_id": user_id,
        "risk_state":
            risk_analysis.get(
                "risk_state"
            ),

        "forecast":
            forecast,

        "notification_strategy":
            notification
    }
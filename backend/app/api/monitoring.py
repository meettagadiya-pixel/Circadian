from fastapi import APIRouter

from app.database.supabase_client import supabase

from app.analytics.timeline_engine import (
    build_health_timeline
)

from app.analytics.forecast_engine import (
    forecast_risk_direction
)

from app.analytics.monitoring_engine import (
    determine_monitoring_frequency
)

router = APIRouter()


@router.get("/monitoring/{user_id}")
def get_monitoring_strategy(user_id: str):

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

    timeline = build_health_timeline(
        snapshots
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

    monitoring = (
        determine_monitoring_frequency(
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

        "monitoring_strategy":
            monitoring
    }
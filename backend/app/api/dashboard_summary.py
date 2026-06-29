from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

from app.api.notification_preview import (
    notification_preview
)

from app.api.adherence_summary import (
    adherence_summary
)

from app.api.readiness_score import (
    readiness_score
)
from app.api.light_exposure_summary import (
    light_exposure_summary
)
from app.api.cgm_summary import (
    cgm_summary
)


router = APIRouter()


@router.get("/dashboard-summary")
def dashboard_summary(
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
            "user_id": user_id
        }

    snapshot = response.data[0]

    data = snapshot.get(
        "snapshot_data",
        {}
    )

    digital_twin = data.get(
        "digital_twin",
        {}
    )

    circadian_phase = digital_twin.get(
        "circadian_phase",
        {}
    )

    metabolic = digital_twin.get(
        "metabolic_analysis",
        {}
    )

    misalignment = data.get(
        "misalignment",
        {}
    )

    trend_analysis = data.get(
        "trend_analysis",
        {}
    )

    risk = data.get(
        "risk_analysis",
        {}
    )

    adherence = data.get(
        "adherence",
        {}
    )

    light_exposure = data.get(
        "light_exposure_analysis",
        {}
    )

    daylight_context = data.get(
        "daylight_context",
        {}
    )

    data_sources = data.get(
        "data_sources",
        {}
    )

    notifications = notification_preview(
        user_id=user_id
    )

    adherence_details = adherence_summary(
        user_id=user_id
    )

    readiness = readiness_score(
        user_id=user_id
    )

    light_details = light_exposure_summary(
        user_id=user_id
    )

    cgm_details = cgm_summary(
        user_id=user_id
    )

    # ─────────────────────────────────────────────────
    # MISALIGNMENT — prefer true social/bio gap
    # Falls back to variability proxy if no
    # behavioral logs were available
    # ─────────────────────────────────────────────────

    misalignment_score = (
        misalignment.get("misalignment_hours")
        or misalignment.get("misalignment_score")
    )

    misalignment_type = misalignment.get(
        "misalignment_type",
        "variability_proxy"
    )

    misalignment_interpretation = misalignment.get(
        "interpretation",
        ""
    )

    return {
        "status": "success",
        "user_id": user_id,
        "summary": {
            "chronotype": digital_twin.get(
                "chronotype"
            ),
            "biological_midnight": circadian_phase.get(
                "biological_midnight"
            ),
            "cbt_nadir_time": circadian_phase.get(
                "cbt_nadir_time"
            ),

            # DLMO estimate: melatonin onset ~2h before biological midnight
            # Based on Lewy et al. (1999) clinical approximation
            # Labelled "estimated" in the UI — not directly measured
            "dlmo_estimate": circadian_phase.get(
                "dlmo_estimate"
            ),

            # TRUE misalignment in hours (social vs bio clock)
            "misalignment_score": misalignment_score,
            "misalignment_hours": misalignment_score,
            "misalignment_type": misalignment_type,
            "misalignment_interpretation": misalignment_interpretation,

            "consistency_score": misalignment.get(
                "consistency_score"
            ),
            "risk_state": risk.get(
                "risk_state"
            ),
            "risk_score": risk.get(
                "risk_score"
            ),
            "avg_hrv": snapshot.get(
                "avg_hrv"
            ),
            "avg_glucose": snapshot.get(
                "avg_glucose"
            ),
            "glucose_variability": metabolic.get(
                "glucose_variability"
            ),
            "meal_adherence": adherence.get(
                "meal_adherence"
            ),
            "exercise_adherence": adherence.get(
                "exercise_adherence"
            ),
            "sleep_adherence": adherence.get(
                "sleep_adherence"
            ),
            "overall_adherence": adherence.get(
                "overall_adherence"
            ),
            "light_exposure_status": light_exposure.get(
                "status"
            ),
            "avg_lux": light_exposure.get(
                "avg_lux"
            ),
            "bright_light_events": light_exposure.get(
                "bright_light_events"
            ),
            "night_light_events": light_exposure.get(
                "night_light_events"
            ),
            "daylight_quality": daylight_context.get(
                "daylight_quality"
            ),
            "clouds": daylight_context.get(
                "clouds"
            ),
            "uvi": daylight_context.get(
                "uvi"
            ),
            "sunrise": daylight_context.get(
                "sunrise"
            ),
            "sunset": daylight_context.get(
                "sunset"
            ),
        },
        "trends": trend_analysis,
        "top_interventions": data.get(
            "zeitgebers",
            []
        ),
        "notifications": notifications.get(
            "notifications",
            []
        ),
        "adherence_summary": adherence_details,
        "readiness": readiness,
        "light_exposure_summary": light_details,
        "cgm_summary": cgm_details,
        "daylight_context": daylight_context,
        "data_sources": data_sources,
        "created_at": snapshot.get(
            "created_at"
        )
    }
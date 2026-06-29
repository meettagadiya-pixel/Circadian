from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


@router.get(
    "/light-exposure-summary"
)
def light_exposure_summary(
    user_id: str
):

    response = (
        supabase
        .table(
            "digital_twin_snapshots"
        )
        .select("*")
        .eq(
            "user_id",
            user_id
        )
        .order(
            "created_at",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if not response.data:

        return {
            "status":
                "no_data",

            "user_id":
                user_id
        }

    snapshot = response.data[0]

    data = snapshot.get(
        "snapshot_data",
        {}
    )

    light = data.get(
        "light_exposure_analysis",
        {}
    )

    status = light.get(
        "status",
        "unknown"
    )

    avg_lux = light.get(
        "avg_lux",
        0
    )

    recommendations = []

    if status == (
        "night_light_exposure"
    ):

        recommendations.append(
            (
                "Reduce screen brightness "
                "and overhead lighting "
                "2–3 hours before sleep."
            )
        )

    if light.get(
        "bright_light_events",
        0
    ) == 0:

        recommendations.append(
            (
                "Increase outdoor light "
                "exposure early in your "
                "biological day."
            )
        )

    if (
        not recommendations
    ):

        recommendations.append(
            (
                "Current light exposure "
                "patterns appear stable."
            )
        )

    return {

        "status":
            "success",

        "user_id":
            user_id,

        "light_exposure": {

            "status":
                status,

            "avg_lux":
                avg_lux,

            "bright_light_events":
                light.get(
                    "bright_light_events"
                ),

            "night_light_events":
                light.get(
                    "night_light_events"
                )
        },

        "recommendations":
            recommendations,

        "created_at":
            snapshot.get(
                "created_at"
            )
    }
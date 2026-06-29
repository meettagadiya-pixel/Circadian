from fastapi import APIRouter

from app.api.dashboard_summary import (
    dashboard_summary
)

router = APIRouter()


@router.get("/daily-insight")
def daily_insight(
    user_id: str
):

    dashboard = dashboard_summary(
        user_id=user_id
    )

    summary = dashboard.get(
        "summary",
        {}
    )

    readiness = dashboard.get(
        "readiness",
        {}
    )

    adherence = dashboard.get(
        "adherence_summary",
        {}
    )

    trends = dashboard.get(
        "trends",
        {}
    )

    readiness_label = readiness.get(
        "readiness_label"
    )

    readiness_score = readiness.get(
        "readiness_score"
    )

    chronotype = summary.get(
        "chronotype"
    )

    overall_adherence = summary.get(
        "overall_adherence"
    )

    trend_items = trends.get(
        "trends",
        []
    )

    main_trend = None

    if trend_items:

        main_trend = trend_items[0].get(
            "message"
        )

    insight = (
        f"Your readiness score today is "
        f"{readiness_score}, which is classified as "
        f"{readiness_label}. "
        f"Your chronotype appears to be {chronotype}. "
    )

    if main_trend:

        insight += (
            f"{main_trend} "
        )

    if overall_adherence is not None:

        insight += (
            f"Your current circadian adherence is "
            f"{round(overall_adherence * 100)}%. "
        )

    recommendations = []

    readiness_recs = readiness.get(
        "recommendations",
        []
    )

    adherence_recs = adherence.get(
        "recommendations",
        []
    )

    recommendations.extend(
        readiness_recs
    )

    recommendations.extend(
        adherence_recs
    )

    return {
        "status": "success",
        "user_id": user_id,
        "insight": insight,
        "recommendations": recommendations,
        "readiness": readiness,
        "adherence": adherence,
        "created_at": dashboard.get(
            "created_at"
        )
    }
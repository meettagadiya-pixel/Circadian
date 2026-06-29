from fastapi import APIRouter

from app.api.dashboard_summary import (
    dashboard_summary
)

router = APIRouter()


@router.get("/coach-recommendation")
def coach_recommendation(
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

    top_interventions = dashboard.get(
        "top_interventions",
        []
    )

    readiness_score = readiness.get(
        "readiness_score"
    )

    readiness_label = readiness.get(
        "readiness_label"
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

    main_issue = None

    if trend_items:

        main_issue = trend_items[0].get(
            "message"
        )

    coach_message = (
        f"Your readiness today is {readiness_score} "
        f"({readiness_label}). "
        f"Your current chronotype pattern appears to be "
        f"{chronotype}. "
    )

    if main_issue:

        coach_message += (
            f"The main issue detected is: "
            f"{main_issue} "
        )

    if overall_adherence is not None:

        coach_message += (
            f"Your circadian adherence score is "
            f"{round(overall_adherence * 100)}%. "
        )

    actions = []

    for item in top_interventions[:3]:

        actions.append(
            item.get(
                "message"
            )
        )

    recommendations = []

    recommendations.extend(
        readiness.get(
            "recommendations",
            []
        )
    )

    recommendations.extend(
        adherence.get(
            "recommendations",
            []
        )
    )

    return {
        "status": "success",
        "user_id": user_id,
        "coach_message": coach_message,
        "top_actions": actions,
        "recommendations": recommendations,
        "readiness": readiness,
        "adherence": adherence,
        "created_at": dashboard.get(
            "created_at"
        )
    }
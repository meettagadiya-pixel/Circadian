from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


def adherence_label(score):

    if score is None:
        return "unknown"
    if score >= 0.8:
        return "strong"
    if score >= 0.6:
        return "moderate"
    if score >= 0.4:
        return "needs_attention"
    return "low"


@router.get("/adherence-summary")
def adherence_summary(user_id: str):

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
    data = snapshot.get("snapshot_data", {})
    adherence = data.get("adherence", {})

    overall  = adherence.get("overall_adherence")
    meal     = adherence.get("meal_adherence")
    exercise = adherence.get("exercise_adherence")
    sleep    = adherence.get("sleep_adherence")

    # No hardcoded recommendations — the zeitgebers
    # already deliver personalised, data-driven guidance.
    # Returning empty list so the frontend Coach section
    # disappears naturally when there is nothing generic to say.

    return {
        "status": "success",
        "user_id": user_id,
        "adherence": {
            "overall_score":   overall,
            "overall_label":   adherence_label(overall),
            "meal_score":      meal,
            "meal_label":      adherence_label(meal),
            "exercise_score":  exercise,
            "exercise_label":  adherence_label(exercise),
            "sleep_score":     sleep,
            "sleep_label":     adherence_label(sleep)
        },
        "recommendations": [],
        "created_at": snapshot.get("created_at")
    }

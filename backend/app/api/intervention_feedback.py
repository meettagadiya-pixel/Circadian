from fastapi import APIRouter

from pydantic import BaseModel

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


class InterventionFeedback(BaseModel):

    user_id: str

    intervention_type: str

    recommendation_message: str

    accepted: bool = False

    ignored: bool = False

    sleep_quality_after: float | None = None

    glucose_after: float | None = None

    recovery_after: float | None = None

    mood_after: float | None = None

    outcome_score: float | None = None


@router.post("/log-intervention-feedback")
def log_intervention_feedback(
    payload: InterventionFeedback
):

    record = {

        "user_id":
            payload.user_id,

        "intervention_type":
            payload.intervention_type,

        "recommendation_message":
            payload.recommendation_message,

        "accepted":
            payload.accepted,

        "ignored":
            payload.ignored,

        "sleep_quality_after":
            payload.sleep_quality_after,

        "glucose_after":
            payload.glucose_after,

        "recovery_after":
            payload.recovery_after,

        "mood_after":
            payload.mood_after,

        "outcome_score":
            payload.outcome_score
    }

    response = (
        supabase
        .table("intervention_outcomes")
        .insert(record)
        .execute()
    )

    return {

        "status":
            "feedback_logged",

        "data":
            response.data
    }
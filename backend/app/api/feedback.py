from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.database.supabase_client import supabase
from app.analytics.outcome_engine import calculate_outcome_score

router = APIRouter()


class InterventionFeedback(BaseModel):
    user_id: str
    intervention_type: str
    recommendation_message: str
    accepted: bool = False
    ignored: bool = False
    sleep_quality_after: Optional[float] = None
    glucose_after: Optional[float] = None
    recovery_after: Optional[float] = None
    mood_after: Optional[float] = None
    outcome_score: Optional[float] = None


@router.post("/feedback")
def save_feedback(feedback: InterventionFeedback):

    feedback_data = feedback.model_dump()

    if feedback_data["outcome_score"] is None:

        feedback_data["outcome_score"] = (
            calculate_outcome_score(
                sleep_quality_after=feedback_data["sleep_quality_after"],
                glucose_after=feedback_data["glucose_after"],
                recovery_after=feedback_data["recovery_after"],
                mood_after=feedback_data["mood_after"]
            )
        )

    response = (
        supabase
        .table("intervention_outcomes")
        .insert(feedback_data)
        .execute()
    )

    return {
        "status": "feedback_saved",
        "data": response.data
    }
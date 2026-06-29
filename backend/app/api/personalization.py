from fastapi import APIRouter

from app.database.supabase_client import supabase

from app.analytics.personalization_engine import (
    analyze_intervention_effectiveness
)

router = APIRouter()


@router.get("/personalization/{user_id}")
def get_personalization(user_id: str):

    response = (
        supabase
        .table("intervention_outcomes")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    recommendations = (
        analyze_intervention_effectiveness(
            response.data
        )
    )

    return {
        "user_id": user_id,
        "personalization_analysis": recommendations
    }
from fastapi import APIRouter

from app.database.supabase_client import supabase
from app.analytics.digital_twin_engine import calculate_user_digital_twin

router = APIRouter()


@router.get("/digital-twin/{user_id}")
def get_digital_twin(user_id: str):
    user_resp = (
        supabase
        .table("users")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    phys_resp = (
        supabase
        .table("physiological_data")
        .select("*")
        .eq("user_id", user_id)
        .order("timestamp")
        .execute()
    )

    behavior_resp = (
    supabase
    .table("behavioral_logs")
    .select("*")
    .eq("user_id", user_id)
    .execute()
    )

    bio_resp = (
    supabase
    .table("biochemical_data")
    .select("*")
    .eq("user_id", user_id)
    .order("timestamp")
    .execute()
    )

    return calculate_user_digital_twin(
        user=user_resp.data,
        physiological_rows=phys_resp.data,
        behavioral_rows=behavior_resp.data,
        biochemical_rows=bio_resp.data
    )
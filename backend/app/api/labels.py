from fastapi import APIRouter

from app.database.supabase_client import supabase
from app.ml.features import build_feature_vector
from app.ml.labels import generate_training_labels

router = APIRouter()


@router.get("/labels/{user_id}")
def get_labels(user_id: str):
    phys_resp = (
        supabase
        .table("physiological_data")
        .select("*")
        .eq("user_id", user_id)
        .order("timestamp")
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

    behavior_resp = (
        supabase
        .table("behavioral_logs")
        .select("*")
        .eq("user_id", user_id)
        .order("timestamp")
        .execute()
    )

    features = build_feature_vector(
        physiological_rows=phys_resp.data,
        biochemical_rows=bio_resp.data,
        behavioral_rows=behavior_resp.data
    )

    labels = generate_training_labels(features)

    return {
        "user_id": user_id,
        "features": features,
        "labels": labels
    }
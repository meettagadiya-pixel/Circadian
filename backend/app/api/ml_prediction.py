from fastapi import APIRouter

from app.database.supabase_client import supabase

from app.ml.features import (
    build_feature_vector
)

from app.ml.train_model import (
    load_or_train_fatigue_model
)

router = APIRouter()


@router.get("/predict-fatigue/{user_id}")
def predict_fatigue(user_id: str):

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

    feature_order = [
        "avg_hrv",
        "avg_rhr",
        "avg_cbt",
        "avg_glucose",
        "glucose_std",
        "max_glucose",
        "sleep_log_count",
        "meal_log_count"
    ]

    input_vector = [
        features.get(col, 0)
        for col in feature_order
    ]

    model_data = load_or_train_fatigue_model()
    model = model_data["model"]

    prediction = model.predict(
        [input_vector]
    )[0]

    probability = model.predict_proba(
        [input_vector]
    )[0].tolist()

    return {
        "user_id": user_id,
        "features": features,
        "fatigue_prediction": int(prediction),
        "prediction_probabilities": probability,
        "model_evaluation": model_data["evaluation"]
    }
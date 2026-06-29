from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


class GlucoseLog(BaseModel):

    user_id: str

    glucose_value: float

    source: str = "manual"

    timestamp: str | None = None


@router.post("/log-glucose")
def log_glucose(
    payload: GlucoseLog
):

    record = {
        "user_id":
            payload.user_id,

        "glucose_value":
            payload.glucose_value,

        "source":
            payload.source,

        "timestamp":
            payload.timestamp
            or
            datetime.utcnow().isoformat()
    }

    response = (
        supabase
        .table("biochemical_data")
        .insert(record)
        .execute()
    )

    return {
        "status": "glucose_logged",
        "data": response.data
    }
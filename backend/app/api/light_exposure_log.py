from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


class LightExposureLog(BaseModel):

    user_id: str

    lux: float

    source: str = "phone_sensor"

    timestamp: str | None = None


@router.post("/log-light-exposure")
def log_light_exposure(
    payload: LightExposureLog
):

    record = {
        "user_id":
            payload.user_id,

        "lux":
            payload.lux,

        "source":
            payload.source,

        "timestamp":
            payload.timestamp
            or
            datetime.utcnow().isoformat()
    }

    response = (
        supabase
        .table("environmental_data")
        .insert(record)
        .execute()
    )

    return {
        "status": "light_exposure_logged",
        "data": response.data
    }
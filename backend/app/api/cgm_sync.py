from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


class CGMReading(BaseModel):

    timestamp: str

    glucose_value: float


class CGMSyncRequest(BaseModel):

    user_id: str

    source: str = "cgm"

    readings: list[CGMReading]


@router.post("/cgm-sync")
def cgm_sync(
    payload: CGMSyncRequest
):

    records = []

    for reading in payload.readings:

        records.append({
            "user_id":
                payload.user_id,

            "timestamp":
                reading.timestamp,

            "glucose_value":
                reading.glucose_value,

            "source":
                payload.source
        })

    if not records:

        return {
            "status": "no_readings",
            "inserted_count": 0,
            "data": []
        }

    response = (
        supabase
        .table("biochemical_data")
        .insert(records)
        .execute()
    )

    return {
        "status": "cgm_synced",
        "source": payload.source,
        "inserted_count": len(response.data),
        "data": response.data,
        "synced_at": datetime.utcnow().isoformat()
    }
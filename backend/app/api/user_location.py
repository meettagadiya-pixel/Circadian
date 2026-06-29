from fastapi import APIRouter
from pydantic import BaseModel

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


class UserLocationPayload(BaseModel):

    user_id: str

    latitude: float

    longitude: float


@router.post("/user-location")
def save_user_location(
    payload: UserLocationPayload
):

    response = (
        supabase
        .table("user_locations")
        .upsert({
            "user_id": payload.user_id,
            "latitude": payload.latitude,
            "longitude": payload.longitude
        })
        .execute()
    )

    return {
        "status": "location_saved",
        "data": response.data
    }
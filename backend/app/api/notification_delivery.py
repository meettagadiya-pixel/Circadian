from fastapi import APIRouter
from pydantic import BaseModel

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


class NotificationDelivery(BaseModel):

    user_id: str

    notification_key: str

    intervention_type: str

    message: str


@router.post("/mark-notification-delivered")
def mark_notification_delivered(
    payload: NotificationDelivery
):

    record = {
        "user_id": payload.user_id,
        "notification_key": payload.notification_key,
        "intervention_type": payload.intervention_type,
        "message": payload.message
    }

    response = (
        supabase
        .table("notification_delivery_log")
        .insert(record)
        .execute()
    )

    return {
        "status": "delivered",
        "data": response.data
    }
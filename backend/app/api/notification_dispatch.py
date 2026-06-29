from fastapi import APIRouter

from pydantic import BaseModel

from app.api.notification_preview import (
    notification_preview
)

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


class NotificationDispatchRequest(BaseModel):

    user_id: str


@router.post("/deliver-current-notifications")
def deliver_current_notifications(
    payload: NotificationDispatchRequest
):

    preview = notification_preview(
        user_id=payload.user_id
    )

    notifications = preview.get(
        "notifications",
        []
    )

    delivered = []

    for item in notifications:

        record = {
            "user_id":
                payload.user_id,

            "notification_key":
                item.get("notification_key"),

            "intervention_type":
                item.get("title"),

            "message":
                item.get("message")
        }

        response = (
            supabase
            .table("notification_delivery_log")
            .insert(record)
            .execute()
        )

        delivered.append(
            response.data[0]
        )

    return {
        "status": "delivered",
        "delivered_count": len(delivered),
        "delivered": delivered
    }
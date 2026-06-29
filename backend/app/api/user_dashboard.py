from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

from app.api.notification_preview import (
    notification_preview
)

from app.api.notification_history import (
    notification_history
)

router = APIRouter()


@router.get("/user-dashboard")
def user_dashboard(
    user_id: str
):

    snapshot_response = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    latest_snapshot = None

    if snapshot_response.data:

        latest_snapshot = snapshot_response.data[0]

    notifications = notification_preview(
        user_id=user_id
    )

    history = notification_history(
        user_id=user_id
    )

    return {
        "status": "success",
        "user_id": user_id,
        "latest_snapshot": latest_snapshot,
        "notifications": notifications,
        "notification_history": history
    }
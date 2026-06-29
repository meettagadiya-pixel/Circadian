from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


@router.get("/notification-history")
def notification_history(
    user_id: str
):

    response = (
        supabase
        .table("notification_delivery_log")
        .select("*")
        .eq("user_id", user_id)
        .order("delivered_at", desc=True)
        .limit(50)
        .execute()
    )

    return {
        "status": "success",
        "user_id": user_id,
        "count": len(response.data),
        "history": response.data
    }
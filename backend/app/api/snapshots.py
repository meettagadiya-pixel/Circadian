from fastapi import APIRouter

from app.database.supabase_client import supabase

router = APIRouter()


@router.get("/snapshots/{user_id}")
def get_snapshots(user_id: str):

    response = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )

    return {
        "user_id": user_id,
        "snapshot_count": len(response.data),
        "snapshots": response.data
    }
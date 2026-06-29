from fastapi import APIRouter

from app.database.supabase_client import supabase

router = APIRouter()


@router.get("/test-db")
def test_database():

    response = (
        supabase
        .table("users")
        .select("*")
        .limit(1)
        .execute()
    )

    return {
        "status": "connected",
        "data": response.data
    }
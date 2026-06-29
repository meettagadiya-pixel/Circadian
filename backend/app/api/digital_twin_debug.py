from fastapi import APIRouter

from app.database.supabase_client import (
    supabase
)

router = APIRouter()


@router.get("/latest-digital-twin")
def latest_digital_twin():

    response = (
        supabase
        .table("digital_twin_snapshots")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:

        return {

            "status":
                "no_data"
        }

    snapshot = response.data[0]

    return {

        "status":
            "success",

        "snapshot":
            snapshot
    }
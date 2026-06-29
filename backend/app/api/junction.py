from fastapi import APIRouter

from app.ingestion.junction_adapter import (
    fetch_junction_data
)

router = APIRouter()


@router.get("/test-junction")
def test_junction():

    return fetch_junction_data(
        user_id="test-user"
    )
from fastapi import APIRouter

from app.ingestion.vital_service import (
    test_vital_connection
)

router = APIRouter()


@router.get("/test-vital")
def test_vital():

    return test_vital_connection()
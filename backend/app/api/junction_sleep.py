from fastapi import APIRouter

from app.ingestion.junction_fetcher import (
    fetch_fitbit_sleep
)

router = APIRouter()


@router.get("/fitbit-sleep")
def get_fitbit_sleep():

    return fetch_fitbit_sleep(
        "5c986070-4eae-457e-917b-5a2ba2713fc6"
    )
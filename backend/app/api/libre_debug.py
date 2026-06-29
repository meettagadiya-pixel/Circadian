from fastapi import APIRouter

from app.ingestion.junction_fetcher import (
    fetch_freestyle_libre_glucose
)

from app.ingestion.junction_parser import (
    summarize_junction_timeseries
)

router = APIRouter()


@router.get("/libre-glucose-debug")
def libre_glucose_debug(
    provider_user_id: str
):

    response = fetch_freestyle_libre_glucose(
        provider_user_id
    )

    summary = summarize_junction_timeseries(
        response
    )

    return {
        "status_code": response.get(
            "status_code"
        ),
        "request_url": response.get(
            "request_url"
        ),
        "summary": summary
    }
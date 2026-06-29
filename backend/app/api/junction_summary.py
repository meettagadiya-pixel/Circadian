from fastapi import APIRouter

from app.ingestion.junction_fetcher import (
    fetch_fitbit_hrv,
    fetch_fitbit_heartrate,
    fetch_fitbit_body_temperature,
    fetch_fitbit_glucose,
    fetch_fitbit_daylight_exposure,
    fetch_fitbit_uv_exposure,
    fetch_fitbit_steps
)

from app.ingestion.junction_parser import (
    summarize_junction_timeseries
)

router = APIRouter()


@router.get("/junction-summary")
def junction_summary(
    provider_user_id: str
):

    return {

        "hrv":
            summarize_junction_timeseries(
                fetch_fitbit_hrv(
                    provider_user_id
                )
            ),

        "heartrate":
            summarize_junction_timeseries(
                fetch_fitbit_heartrate(
                    provider_user_id
                )
            ),

        "body_temperature":
            summarize_junction_timeseries(
                fetch_fitbit_body_temperature(
                    provider_user_id
                )
            ),

        "glucose":
            summarize_junction_timeseries(
                fetch_fitbit_glucose(
                    provider_user_id
                )
            ),

        "daylight_exposure":
            summarize_junction_timeseries(
                fetch_fitbit_daylight_exposure(
                    provider_user_id
                )
            ),

        "uv_exposure":
            summarize_junction_timeseries(
                fetch_fitbit_uv_exposure(
                    provider_user_id
                )
            ),

        "steps":
            summarize_junction_timeseries(
                fetch_fitbit_steps(
                    provider_user_id
                )
            )
    }
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

router = APIRouter()


@router.get("/junction-debug")
def junction_debug(
    provider_user_id: str
):

    hrv = fetch_fitbit_hrv(
        provider_user_id
    )

    heartrate = fetch_fitbit_heartrate(
        provider_user_id
    )

    body_temperature = (
        fetch_fitbit_body_temperature(
            provider_user_id
        )
    )

    glucose = (
        fetch_fitbit_glucose(
            provider_user_id
        )
    )

    daylight = (
        fetch_fitbit_daylight_exposure(
            provider_user_id
        )
    )

    uv = (
        fetch_fitbit_uv_exposure(
            provider_user_id
        )
    )

    steps = (
        fetch_fitbit_steps(
            provider_user_id
        )
    )

    return {
        "hrv":
            hrv["status_code"],

        "heartrate":
            heartrate["status_code"],

        "body_temperature":
            body_temperature[
                "status_code"
            ],

        "glucose":
            glucose[
                "status_code"
            ],

        "daylight_exposure":
            daylight[
                "status_code"
            ],

        "uv_exposure":
            uv[
                "status_code"
            ],

        "steps":
            steps[
                "status_code"
            ]
    }
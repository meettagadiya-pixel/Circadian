import requests

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.post("/connect-fitbit-demo")
def connect_fitbit_demo():

    url = (
        f"{settings.VITAL_BASE_URL}"
        "/v2/link/connect/demo"
    )

    headers = {
        "x-vital-api-key":
            settings.VITAL_API_KEY,

        "Content-Type":
            "application/json"
    }

    payload = {
        "user_id":
            "5c986070-4eae-457e-917b-5a2ba2713fc6",

        "provider":
            "fitbit"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return {
        "status_code":
            response.status_code,

        "response":
            response.text
    }
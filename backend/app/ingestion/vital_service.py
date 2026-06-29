import requests

from app.core.config import settings


def get_vital_headers():
    return {
        "x-vital-api-key": settings.VITAL_API_KEY.strip(),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def test_vital_connection():
    url = f"{settings.VITAL_BASE_URL}/v2/introspect/resources"

    response = requests.get(
        url,
        headers=get_vital_headers()
    )

    try:
        data = response.json()
    except:
        data = response.text

    return {
        "status_code": response.status_code,
        "response": data
    }
import requests

from app.core.config import settings


def fetch_junction_data(
    user_id
):

    headers = {
        "x-vital-api-key":
            settings.VITAL_API_KEY,

        "Accept":
            "application/json"
    }

    url = (
        f"{settings.VITAL_BASE_URL}"
        "/v2/introspect/resources"
    )

    try:

        print(
            "Using API key prefix:",
            settings.VITAL_API_KEY[:10]
        )

        print(
            "Using URL:",
            url
        )

        response = requests.get(
            url,
            headers=headers
        )

        return {

            "provider":
                "junction",

            "connected":
                response.status_code == 200,

            "status_code":
                response.status_code,

            "response_headers":
                dict(response.headers),

            "response_text":
                response.text,

            "request_url":
                url
        }

    except Exception as e:

        return {

            "provider":
                "junction",

            "connected":
                False,

            "error":
                str(e),

            "request_url":
                url
        }
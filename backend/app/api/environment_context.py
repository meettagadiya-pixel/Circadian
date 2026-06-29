import os
import requests

from fastapi import APIRouter

router = APIRouter()


@router.get("/environment-context")
def environment_context(
    latitude: float,
    longitude: float
):

    api_key = os.getenv(
        "OPENWEATHER_API_KEY"
    )

    if not api_key:

        return {
            "status": "missing_api_key",
            "message": "OPENWEATHER_API_KEY is not set"
        }

    url = (
        "https://api.openweathermap.org/data/3.0/onecall"
        f"?lat={latitude}"
        f"&lon={longitude}"
        "&exclude=minutely,hourly,alerts"
        "&units=metric"
        f"&appid={api_key}"
    )

    try:

        response = requests.get(
            url,
            timeout=20
        )

        data = response.json()
        if response.status_code != 200:

            return {
                "status": "weather_api_error",
                "status_code": response.status_code,
                "message": data,
                "latitude": latitude,
                "longitude": longitude
            }

    except Exception as error:

        return {
            "status": "weather_api_error",
            "message": str(error),
            "latitude": latitude,
            "longitude": longitude
        }

    current = data.get(
        "current",
        {}
    )

    return {
        "status": "success",
        "latitude": latitude,
        "longitude": longitude,
        "sunrise": current.get("sunrise"),
        "sunset": current.get("sunset"),
        "temperature": current.get("temp"),
        "clouds": current.get("clouds"),
        "uvi": current.get("uvi"),
        "weather": current.get("weather", [])
    }
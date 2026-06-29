import requests


def fetch_light_cycle():

    latitude = 51.5072
    longitude = -0.1276

    url = (

        "https://api.open-meteo.com/v1/forecast"

        f"?latitude={latitude}"

        f"&longitude={longitude}"

        "&daily=sunrise,sunset"

        "&timezone=auto"
    )

    response = requests.get(
        url
    )

    data = response.json()

    daily = data.get(
        "daily",
        {}
    )

    sunrise = daily.get(
        "sunrise",
        []
    )[0]

    sunset = daily.get(
        "sunset",
        []
    )[0]

    return {

        "sunrise":
            sunrise,

        "sunset":
            sunset
    }
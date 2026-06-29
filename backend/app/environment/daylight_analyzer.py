from dateutil.parser import parse
from datetime import datetime, timezone


def analyze_daylight_context(
    sunrise,
    sunset,
    biological_midnight,
    clouds=None,
    uvi=None,
    weather=None
):

    if (
        not sunrise
        or
        not sunset
        or
        not biological_midnight
    ):

        return {
            "status": "no_daylight_context"
        }

    if isinstance(sunrise, int):
        sunrise_dt = datetime.fromtimestamp(
            sunrise,
            tz=timezone.utc
        )
    else:
        sunrise_dt = parse(sunrise)

    if isinstance(sunset, int):
        sunset_dt = datetime.fromtimestamp(
            sunset,
            tz=timezone.utc
        )
    else:
        sunset_dt = parse(sunset)

    midnight_dt = parse(
        biological_midnight
    )

    midnight_hour = (
        midnight_dt.hour
        +
        midnight_dt.minute / 60
    )

    sunrise_hour = (
        sunrise_dt.hour
        +
        sunrise_dt.minute / 60
    )

    sunset_hour = (
        sunset_dt.hour
        +
        sunset_dt.minute / 60
    )

    sunrise_offset_hours = round(
        sunrise_hour
        -
        midnight_hour,
        2
    )

    sunset_offset_hours = round(
        sunset_hour
        -
        midnight_hour,
        2
    )

    daylight_quality = "normal"

    if clouds is not None and clouds >= 70:
        daylight_quality = "low_natural_light"

    elif uvi is not None and uvi >= 6:
        daylight_quality = "strong_sunlight"

    recommendations = []

    if daylight_quality == "low_natural_light":

        recommendations.append(
            "Cloud cover may reduce natural light exposure today. Spend longer outdoors or use bright indoor light earlier in the day."
        )

    elif daylight_quality == "strong_sunlight":

        recommendations.append(
            "Natural light is strong today. A shorter morning outdoor light session may be sufficient."
        )

    else:

        recommendations.append(
            "Natural daylight conditions appear suitable for regular morning light exposure."
        )

    return {
        "status": "success",
        "sunrise": sunrise_dt.isoformat(),
        "sunset": sunset_dt.isoformat(),
        "sunrise_offset_from_biological_midnight": sunrise_offset_hours,
        "sunset_offset_from_biological_midnight": sunset_offset_hours,
        "clouds": clouds,
        "uvi": uvi,
        "weather": weather,
        "daylight_quality": daylight_quality,
        "recommendations": recommendations
    }
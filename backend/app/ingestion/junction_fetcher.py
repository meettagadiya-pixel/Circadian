import requests

from app.core.config import settings


DEFAULT_START_DATE = "2026-05-17"
DEFAULT_END_DATE   = "2026-06-16"

DEFAULT_PROVIDER = (
    "fitbit"
)


# ---------------------------------
# GENERIC REQUEST
# ---------------------------------


def _make_request(

    url,
    provider=DEFAULT_PROVIDER,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE
):

    headers = {

        "x-vital-api-key":
            settings.VITAL_API_KEY
    }

    params = {

        "provider":
            provider,

        "start_date":
            start_date,

        "end_date":
            end_date
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
    )

    except Exception as error:

        return {
            "status_code": 0,
            "request_url": url,
            "data": {},
            "error": str(error)
        }

    try:

        data = response.json()

    except Exception:

        data = response.text

    return {

        "status_code":
            response.status_code,

        "request_url":
            response.url,

        "data":
            data
    }


# ---------------------------------
# SUMMARY ENDPOINTS
# ---------------------------------


def fetch_junction_summary(

    user_id,
    endpoint,
    provider=DEFAULT_PROVIDER
):

    url = (
        f"{settings.VITAL_BASE_URL}"
        f"/v2/summary/"
        f"{endpoint}/"
        f"{user_id}"
    )

    print(
        f"Fetching summary {endpoint}:",
        url
    )

    return _make_request(

        url,

        provider=provider
    )


def fetch_fitbit_activity(
    user_id
):

    return fetch_junction_summary(

        user_id=user_id,

        endpoint="activity"
    )


def fetch_fitbit_sleep(
    user_id
):

    return fetch_junction_summary(

        user_id=user_id,

        endpoint="sleep"
    )


# ---------------------------------
# TIMESERIES ENDPOINTS
# ---------------------------------


def fetch_junction_timeseries(

    user_id,
    endpoint,
    provider=DEFAULT_PROVIDER
):

    url = (
        f"{settings.VITAL_BASE_URL}"
        f"/v2/timeseries/"
        f"{user_id}/"
        f"{endpoint}/grouped"
    )

    print(
        f"Fetching timeseries "
        f"{endpoint}:",
        url
    )

    return _make_request(

        url,

        provider=provider
    )


# ---------------------------------
# FITBIT
# ---------------------------------


def fetch_fitbit_heartrate(
    user_id
):

    return fetch_junction_timeseries(

        user_id=user_id,

        endpoint="heartrate"
    )


def fetch_fitbit_hrv(
    user_id
):

    return fetch_junction_timeseries(

        user_id=user_id,

        endpoint="hrv"
    )


def fetch_fitbit_body_temperature(
    user_id
):

    return fetch_junction_timeseries(

        user_id=user_id,

        endpoint="body_temperature"
    )


def fetch_fitbit_glucose(
    user_id
):

    return fetch_junction_timeseries(

        user_id=user_id,

        endpoint="glucose"
    )


def fetch_fitbit_daylight_exposure(
    user_id
):

    return fetch_junction_timeseries(

        user_id=user_id,

        endpoint="daylight_exposure"
    )


def fetch_fitbit_uv_exposure(
    user_id
):

    return fetch_junction_timeseries(

        user_id=user_id,

        endpoint="uv_exposure"
    )


def fetch_fitbit_steps(
    user_id
):

    return fetch_junction_timeseries(

        user_id=user_id,

        endpoint="steps"
    )


# ---------------------------------
# FREESTYLE LIBRE
# ---------------------------------


def fetch_freestyle_libre_glucose(
    user_id
):

    return fetch_junction_timeseries(

        user_id=user_id,

        endpoint="glucose",

        provider="freestyle_libre"
    )
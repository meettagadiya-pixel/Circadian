def fetch_vital_data(
    user_id
):

    # -------------------------
    # FUTURE VITAL API
    # -------------------------

    # This adapter will later:
    # - authenticate with Vital
    # - fetch wearable biomarker data
    # - normalize payloads
    # - return standardized physiology

    return {
        "provider": "vital",
        "connected": False,
        "data": None
    }
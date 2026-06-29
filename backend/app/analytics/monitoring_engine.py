def determine_monitoring_frequency(
    risk_state,
    forecast_direction
):

    if risk_state == "critical":

        return {
            "monitoring_level":
                "continuous",

            "recommended_interval_minutes":
                5
        }

    elif risk_state == "high":

        return {
            "monitoring_level":
                "high_frequency",

            "recommended_interval_minutes":
                15
        }

    elif (
        risk_state == "moderate"
        and forecast_direction == "worsening"
    ):

        return {
            "monitoring_level":
                "elevated",

            "recommended_interval_minutes":
                30
        }

    else:

        return {
            "monitoring_level":
                "standard",

            "recommended_interval_minutes":
                60
        }
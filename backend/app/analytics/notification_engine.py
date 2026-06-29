def generate_notification_strategy(
    risk_state,
    forecast_direction
):

    if (
        risk_state == "critical"
    ):

        return {
            "notification_level":
                "urgent",

            "send_notification":
                True,

            "message":
                (
                    "Critical physiological "
                    "recovery recommended."
                )
        }

    elif (
        risk_state == "high"
    ):

        return {
            "notification_level":
                "high_priority",

            "send_notification":
                True,

            "message":
                (
                    "Physiological strain "
                    "is elevated today."
                )
        }

    elif (
        risk_state == "moderate"
        and forecast_direction == "worsening"
    ):

        return {
            "notification_level":
                "preventive",

            "send_notification":
                True,

            "message":
                (
                    "Recovery behaviors may "
                    "help prevent worsening."
                )
        }

    else:

        return {
            "notification_level":
                "silent",

            "send_notification":
                False,

            "message":
                (
                    "No notification needed."
                )
        }
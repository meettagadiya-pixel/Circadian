def aggregate_physiology(
    normalized_activity
):

    if not normalized_activity:

        return {

            "avg_activity_score": 0,

            "avg_recovery_score": 0,

            "avg_fatigue_risk": 0
        }

    total_activity = 0
    total_recovery = 0
    total_fatigue = 0

    count = len(
        normalized_activity
    )

    for item in normalized_activity:

        total_activity += item.get(
            "activity_score",
            0
        )

        total_recovery += item.get(
            "recovery_score",
            0
        )

        total_fatigue += item.get(
            "fatigue_risk",
            0
        )

    return {

        "avg_activity_score":
            round(
                total_activity / count,
                2
            ),

        "avg_recovery_score":
            round(
                total_recovery / count,
                2
            ),

        "avg_fatigue_risk":
            round(
                total_fatigue / count,
                2
            )
    }
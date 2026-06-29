def normalize_activity(
    activity
):

    steps = activity.get(
        "steps",
        0
    )

    active_calories = activity.get(
        "calories_active",
        0
    )

    active_calories = max(
        active_calories,
        0
    )

    heart_rate = activity.get(
        "heart_rate"
    ) or {}

    resting_hr = heart_rate.get(
        "resting_bpm"
    )

    if resting_hr is None:
        resting_hr = 60

    distance = activity.get(
        "distance",
        0
    )

    activity_score = min(
        steps / 10000,
        1.0
    )

    cardio_load = min(
        active_calories / 600,
        1.0
    )

    recovery_score = max(
        0,
        1 - (
            resting_hr - 55
        ) / 40
    )

    fatigue_risk = (
        cardio_load * 0.5
        +
        (1 - recovery_score) * 0.5
    )

    fatigue_risk = max(
        fatigue_risk,
        0
    )

    return {

        "steps":
            steps,

        "distance":
            distance,

        "active_calories":
            active_calories,

        "resting_hr":
            resting_hr,

        "activity_score":
            round(activity_score, 2),

        "cardio_load":
            round(cardio_load, 2),

        "recovery_score":
            round(recovery_score, 2),

        "fatigue_risk":
            round(fatigue_risk, 2)
    }
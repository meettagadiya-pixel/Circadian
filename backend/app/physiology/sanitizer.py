def sanitize_activity(
    activity
):

    resting_hr = activity.get(
        "resting_hr",
        60
    )

    active_calories = activity.get(
        "active_calories",
        0
    )

    steps = activity.get(
        "steps",
        0
    )

    if resting_hr < 30 or resting_hr > 120:
        resting_hr = 60

    if active_calories < 0:
        active_calories = 0

    if steps < 0:
        steps = 0

    activity["resting_hr"] = resting_hr
    activity["active_calories"] = active_calories
    activity["steps"] = steps

    return activity
from datetime import datetime
from dateutil.parser import parse


def analyze_meal_timing(
    behavioral_rows,
    biological_midnight
):

    if not behavioral_rows:

        return {

            "status":
                "no_behavioral_data"
        }

    late_meals = 0
    total_meals = 0

    midnight_hour = (
        datetime.fromisoformat(
            biological_midnight
        ).hour
    )

    for row in behavioral_rows:

        timestamp = row.get(
            "timestamp"
        )

        meal_type = row.get(
            "event_type"
        )

        if (
            not timestamp
            or
            meal_type != "meal"
        ):
            continue

        total_meals += 1

        meal_hour = parse(
            timestamp
        ).hour
        

        hour_distance = abs(
            meal_hour
            -
            midnight_hour
        )

        if hour_distance <= 3:

            late_meals += 1

    if total_meals == 0:

        return {

            "status":
                "no_meals_logged"
        }

    late_ratio = (
        late_meals
        /
        total_meals
    )

    status = (
        "aligned"
        if late_ratio < 0.3
        else "late_eating_pattern"
    )

    return {

        "status":
            status,

        "late_meal_ratio":
            round(
                late_ratio,
                2
            ),

        "late_meals":
            late_meals,

        "total_meals":
            total_meals
    }
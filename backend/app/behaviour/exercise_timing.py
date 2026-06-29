from dateutil.parser import parse


def analyze_exercise_timing(
    behavioral_rows,
    biological_midnight
):

    if not behavioral_rows:

        return {

            "status":
                "no_behavioral_data"
        }

    bio_midnight_hour = (
        parse(
            biological_midnight
        ).hour
    )

    late_exercise_count = 0

    total_exercise = 0

    for row in behavioral_rows:

        event_type = row.get(
            "event_type"
        )

        if event_type != "exercise":

            continue

        total_exercise += 1

        timestamp = row.get(
            "timestamp"
        )

        if not timestamp:

            continue

        exercise_hour = (
            parse(
                timestamp
            ).hour
        )

        hour_distance = abs(
            exercise_hour
            -
            bio_midnight_hour
        )

        if hour_distance <= 3:

            late_exercise_count += 1

    if total_exercise == 0:

        return {

            "status":
                "no_exercise_logged"
        }

    ratio = (
        late_exercise_count
        /
        total_exercise
    )

    if ratio >= 0.5:

        status = (
            "late_exercise_pattern"
        )

    else:

        status = (
            "exercise_timing_stable"
        )

    return {

        "status":
            status,

        "late_exercise_ratio":
            round(ratio, 2),

        "late_exercise_count":
            late_exercise_count,

        "total_exercise":
            total_exercise
    }
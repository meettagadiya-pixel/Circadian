from datetime import timezone
from dateutil.parser import parse


def calculate_adherence_score(
    behavioral_logs,
    biological_midnight
):
    """
    Calculates adherence scores for meal, exercise and sleep
    based on how well the user's behavior aligns with their
    biological clock (biological midnight).

    Sleep adherence uses a GRADIENT scoring approach:
    - Sleeping within 2h of bio midnight = full score
    - Sleeping 2-4h away = partial score
    - Sleeping 4-6h away = low but non-zero score
    - More than 6h away = minimum score

    This is more honest than binary pass/fail which produced
    0% for someone with high misalignment.
    """

    midnight_dt = parse(biological_midnight)

    if midnight_dt.tzinfo is None:
        midnight_dt = midnight_dt.replace(tzinfo=timezone.utc)

    meal_total = 0
    meal_good = 0

    exercise_total = 0
    exercise_good = 0

    sleep_total = 0
    sleep_score_sum = 0.0

    for log in behavioral_logs:

        event_type = log.get("event_type", "")
        timestamp = log.get("timestamp")

        if not timestamp:
            continue

        ts = parse(timestamp)

        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        hours_from_midnight = (
            ts - midnight_dt
        ).total_seconds() / 3600

        # ─────────────────────────────────────────
        # MEAL ADHERENCE
        # Good meals: eaten during the biological day
        # (8h before midnight to 4h after midnight)
        # ─────────────────────────────────────────
        if event_type == "meal":

            meal_total += 1

            if -8 <= hours_from_midnight <= 4:
                meal_good += 1

        # ─────────────────────────────────────────
        # EXERCISE ADHERENCE
        # Good exercise: not within 3h of biological midnight
        # (exercising close to bio midnight disrupts sleep)
        # ─────────────────────────────────────────
        elif event_type == "exercise":

            exercise_total += 1

            if -12 <= hours_from_midnight <= 2:
                exercise_good += 1

        # ─────────────────────────────────────────
        # SLEEP ADHERENCE — GRADIENT SCORING
        # Instead of binary pass/fail, score how close
        # the sleep onset is to biological midnight
        #
        # Ideal: sleep onset 6-8h before biological midnight
        # (i.e. hours_from_midnight = -6 to -8)
        # Since bio midnight is the MIDPOINT of sleep,
        # ideal sleep onset is ~4h before it
        # ─────────────────────────────────────────
        elif event_type == "sleep_onset":

            sleep_total += 1

            abs_gap = abs(hours_from_midnight)

            # Ideal: within 2h of bio midnight
            if abs_gap <= 2:
                sleep_score_sum += 1.0

            # Close: 2-3h away
            elif abs_gap <= 3:
                sleep_score_sum += 0.75

            # Moderate: 3-4h away
            elif abs_gap <= 4:
                sleep_score_sum += 0.55

            # High misalignment: 4-5h away
            elif abs_gap <= 5:
                sleep_score_sum += 0.35

            # Very high misalignment: 5-6h away
            elif abs_gap <= 6:
                sleep_score_sum += 0.20

            # Extreme misalignment: >6h away
            else:
                sleep_score_sum += 0.10

    # ─────────────────────────────────────────
    # FINAL SCORES
    # ─────────────────────────────────────────

    meal_score = (
        meal_good / meal_total
        if meal_total else 0
    )

    exercise_score = (
        exercise_good / exercise_total
        if exercise_total else 0
    )

    sleep_score = (
        sleep_score_sum / sleep_total
        if sleep_total else 0
    )

    overall_score = (
        meal_score
        + exercise_score
        + sleep_score
    ) / 3

    return {
        "meal_adherence": round(meal_score, 2),
        "exercise_adherence": round(exercise_score, 2),
        "sleep_adherence": round(sleep_score, 2),
        "overall_adherence": round(overall_score, 2)
    }

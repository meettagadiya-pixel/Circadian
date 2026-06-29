def calculate_outcome_score(
    sleep_quality_after=None,
    glucose_after=None,
    recovery_after=None,
    mood_after=None
):

    scores = []

    if sleep_quality_after is not None:
        scores.append(
            sleep_quality_after
        )

    if recovery_after is not None:
        scores.append(
            recovery_after
        )

    if mood_after is not None:
        scores.append(
            mood_after
        )

    if glucose_after is not None:

        glucose_score = max(
            0,
            min(
                1,
                (140 - glucose_after) / 60
            )
        )

        scores.append(glucose_score)

    if not scores:
        return None

    return round(
        sum(scores) / len(scores),
        2
    )
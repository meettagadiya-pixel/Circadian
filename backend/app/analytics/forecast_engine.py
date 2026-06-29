import pandas as pd


def forecast_risk_direction(
    timeline
):

    if len(timeline) < 5:

        return {
            "status":
                "not_enough_data"
        }

    df = pd.DataFrame(timeline)

    risk_scores = (
        df["risk_score"]
        .fillna(0)
        .astype(float)
        .tolist()
    )

    recent = risk_scores[-3:]

    trend = (
        recent[-1]
        - recent[0]
    )

    if trend > 10:

        direction = "rapidly_worsening"

    elif trend > 3:

        direction = "worsening"

    elif trend < -5:

        direction = "improving"

    else:

        direction = "stable"

    predicted_next = (
        recent[-1]
        + trend
    )

    return {
        "risk_direction":
            direction,

        "current_risk":
            recent[-1],

        "predicted_next_risk":
            round(predicted_next, 2)
    }
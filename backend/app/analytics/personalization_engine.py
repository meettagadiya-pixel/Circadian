import pandas as pd


def analyze_intervention_effectiveness(
    intervention_rows
):

    if not intervention_rows:
        return []

    df = pd.DataFrame(
        intervention_rows
    )

    recommendations = []

    grouped = (
        df.groupby("intervention_type")
    )

    for intervention_type, group in grouped:

        avg_outcome = (
            group["outcome_score"]
            .astype(float)
            .mean()
        )

        recommendations.append({
            "intervention_type": intervention_type,
            "average_outcome_score": round(
                avg_outcome,
                2
            ),
            "recommendation_count": len(group)
        })

    recommendations = sorted(
        recommendations,
        key=lambda x: x["average_outcome_score"],
        reverse=True
    )

    return recommendations
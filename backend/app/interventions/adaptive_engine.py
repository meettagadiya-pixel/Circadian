def rank_interventions(
    zeitgebers,
    personalization_data
):

    if not personalization_data:
        return zeitgebers

    score_lookup = {}

    for item in personalization_data:

        score_lookup[
            item["intervention_type"]
        ] = item[
            "average_outcome_score"
        ]

    ranked = sorted(
        zeitgebers,
        key=lambda z: score_lookup.get(
            z["type"],
            0
        ),
        reverse=True
    )

    return ranked
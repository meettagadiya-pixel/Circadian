def prioritize_interventions(
    interventions
):

    if not interventions:

        return []

    priority_weights = {

        "high": 3,

        "medium": 2,

        "low": 1
    }

    # -------------------------
    # SCORE INTERVENTIONS
    # -------------------------

    scored = []

    seen_messages = set()

    for item in interventions:

        message = item.get(
            "message",
            ""
        )

        # REMOVE DUPLICATES

        if message in seen_messages:

            continue

        seen_messages.add(
            message
        )

        priority = item.get(
            "priority",
            "low"
        )

        score = priority_weights.get(
            priority,
            1
        )

        scored.append({

            "score":
                score,

            "data":
                item
        })

    # -------------------------
    # SORT DESCENDING
    # -------------------------

    scored.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # -------------------------
    # RETURN TOP 3
    # -------------------------

    top = [

        item["data"]

        for item in scored[:3]
    ]

    return top
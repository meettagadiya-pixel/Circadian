def analyze_circadian_trends(
    circadian_analysis
):

    if len(
        circadian_analysis
    ) < 2:

        return {

            "trend":
                "insufficient_data"
        }

    recovery_scores = []
    alignment_scores = []
    sleep_hours = []

    for item in circadian_analysis:

        recovery_scores.append(
            item.get(
                "recovery_score",
                0
            )
        )

        alignment_scores.append(
            item.get(
                "circadian_alignment",
                0
            )
        )

        sleep_hours.append(
            item.get(
                "sleep_hours",
                0
            )
        )

    recovery_delta = (
        recovery_scores[-1]
        -
        recovery_scores[0]
    )

    alignment_delta = (
        alignment_scores[-1]
        -
        alignment_scores[0]
    )

    sleep_delta = (
        sleep_hours[-1]
        -
        sleep_hours[0]
    )

    trends = []

    if recovery_delta < -0.1:

        trends.append({

            "type":
                "recovery_decline",

            "severity":
                "medium",

            "message":
                (
                    "Recovery trends appear to be worsening."
                )
        })

    if alignment_delta < -0.1:

        trends.append({

            "type":
                "circadian_instability",

            "severity":
                "high",

            "message":
                (
                    "Circadian alignment appears "
                    "to be deteriorating."
                )
        })

    if sleep_delta < -1:

        trends.append({

            "type":
                "sleep_reduction",

            "severity":
                "medium",

            "message":
                (
                    "Sleep duration has declined "
                    "significantly."
                )
        })

    if not trends:

        trends.append({

            "type":
                "stable",

            "severity":
                "low",

            "message":
                (
                    "Circadian trends appear stable."
                )
        })

    return {

        "recovery_delta":
            round(
                recovery_delta,
                2
            ),

        "alignment_delta":
            round(
                alignment_delta,
                2
            ),

        "sleep_delta":
            round(
                sleep_delta,
                2
            ),

        "trends":
            trends
    }
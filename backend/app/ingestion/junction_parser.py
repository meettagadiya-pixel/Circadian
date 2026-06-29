def extract_timeseries_values(
    response
):

    values = []

    data = response.get(
        "data",
        {}
    )

    groups = data.get(
        "groups",
        {}
    )

    for provider_groups in groups.values():

        for group in provider_groups:

            readings = group.get(
                "data",
                []
            )

            for item in readings:

                value = item.get(
                    "value"
                )

                timestamp = item.get(
                    "timestamp"
                )

                if value is None:
                    continue

                values.append({
                    "timestamp": timestamp,
                    "value": float(value),
                    "unit": item.get(
                        "unit"
                    )
                })

    return values


def summarize_junction_timeseries(
    response
):

    values = extract_timeseries_values(
        response
    )

    if not values:

        return {
            "count": 0,
            "avg": None,
            "max": None,
            "latest": None
        }

    numeric_values = [
        item["value"]
        for item in values
    ]

    return {
        "count": len(values),

        "avg": round(
            sum(numeric_values)
            /
            len(numeric_values),
            2
        ),

        "max": round(
            max(numeric_values),
            2
        ),

        "latest": values[-1]
    }
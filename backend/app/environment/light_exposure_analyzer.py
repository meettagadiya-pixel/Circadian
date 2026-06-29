from dateutil.parser import parse


def analyze_light_exposure(
    environmental_rows,
    biological_midnight
):

    if not environmental_rows:

        return {
            "status": "no_light_data",
            "avg_lux": 0,
            "bright_light_events": 0,
            "night_light_events": 0
        }

    biological_midnight_dt = parse(
        biological_midnight
    )

    lux_values = []
    bright_light_events = 0
    night_light_events = 0

    for row in environmental_rows:

        lux = (
            row.get("lux")
            or
            row.get("lux_exposure")
        )

        timestamp = row.get(
            "timestamp"
        )

        if lux is None or not timestamp:
            continue

        lux = float(
            lux
        )

        ts = parse(
            timestamp
        )

        lux_values.append(
            lux
        )

        hours_from_midnight = (
            ts - biological_midnight_dt
        ).total_seconds() / 3600

        if lux >= 500:

            bright_light_events += 1

        if (
            -3
            <= hours_from_midnight
            <= 3
            and lux >= 100
        ):

            night_light_events += 1

    avg_lux = (
        round(
            sum(lux_values) / len(lux_values),
            2
        )
        if lux_values
        else 0
    )

    status = "light_exposure_stable"

    if night_light_events > 0:

        status = "night_light_exposure"

    return {
        "status": status,
        "avg_lux": avg_lux,
        "bright_light_events": bright_light_events,
        "night_light_events": night_light_events
    }
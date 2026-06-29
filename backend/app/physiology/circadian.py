from datetime import (
    datetime,
    timedelta
)


def estimate_circadian_phase(
    sleep
):

    bedtime = sleep.get(
        "bedtime_start"
    )

    wake = sleep.get(
        "bedtime_stop"
    )

    duration = sleep.get(
        "total",
        0
    )

    efficiency = sleep.get(
        "efficiency",
        0
    )

    hrv = sleep.get(
        "average_hrv"
    )

    if hrv is None:
        hrv = 20

    bedtime_dt = datetime.fromisoformat(
        bedtime.replace(
            "Z",
            "+00:00"
        )
    )

    wake_dt = datetime.fromisoformat(
        wake.replace(
            "Z",
            "+00:00"
        )
    )

    midpoint = bedtime_dt + (
        wake_dt - bedtime_dt
    ) / 2

    sleep_hours = round(
        duration / 3600,
        2
    )

    recovery_score = min(
        hrv / 40,
        1.0
    )

    circadian_alignment = min(
        efficiency / 100,
        1.0
    )

    return {

        "sleep_hours":
            sleep_hours,

        "sleep_midpoint":
            midpoint.isoformat(),

        "efficiency":
            efficiency,

        "hrv":
            hrv,

        "recovery_score":
            round(
                recovery_score,
                2
            ),

        "circadian_alignment":
            round(
                circadian_alignment,
                2
            )
    }
from dateutil.parser import parse

from datetime import timedelta


def schedule_interventions(

    interventions,

    circadian_phase,

    sunrise_data
):

    scheduled = []

    biological_midnight = parse(
        circadian_phase[
            "biological_midnight"
        ]
    )

    sunrise = parse(
        sunrise_data[
            "sunrise"
        ]
    )

    for item in interventions:

        intervention_type = item.get(
            "type"
        )

        scheduled_time = None

        # -------------------------
        # LIGHT EXPOSURE
        # -------------------------

        if intervention_type == (
            "light_exposure"
        ):

            scheduled_time = (
                sunrise
                +
                timedelta(minutes=30)
            )

        # -------------------------
        # EXERCISE TIMING
        # -------------------------

        elif intervention_type == (
            "exercise_timing"
        ):

            scheduled_time = (
                biological_midnight
                -
                timedelta(hours=4)
            )

        # -------------------------
        # NUTRITION
        # -------------------------

        elif intervention_type == (
            "nutrition"
        ):

            scheduled_time = (
                biological_midnight
                -
                timedelta(hours=3)
            )

        # -------------------------
        # SLEEP SCHEDULE
        # -------------------------

        elif intervention_type == (
            "sleep_schedule"
        ):

            scheduled_time = (
                biological_midnight
                -
                timedelta(hours=2)
            )

        # -------------------------
        # DEFAULT
        # -------------------------

        else:

            scheduled_time = (
                biological_midnight
                -
                timedelta(hours=1)
            )

        enriched = {

            **item,

            "scheduled_time":
                scheduled_time.isoformat()
        }

        scheduled.append(
            enriched
        )

    return scheduled
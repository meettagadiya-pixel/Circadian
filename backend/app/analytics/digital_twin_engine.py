import pandas as pd
from datetime import timedelta


def calculate_biological_midnight(
    physiological_rows
):

    if not physiological_rows:

        return None

    df = pd.DataFrame(
        physiological_rows
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["core_body_temp"] = pd.to_numeric(
        df["core_body_temp"]
    )

    df = df.sort_values(
        "timestamp"
    )

    df["smoothed_temp"] = (
        df["core_body_temp"]
        .rolling(
            window=3,
            min_periods=1
        )
        .mean()
    )

    nadir_row = df.loc[
        df["smoothed_temp"].idxmin()
    ]

    nadir_time = nadir_row[
        "timestamp"
    ]

    biological_midnight = (
        nadir_time
        -
        timedelta(hours=3)
    )

    # DLMO (Dim Light Melatonin Onset) estimate:
    # DLMO ≈ biological_midnight - 2 hours
    # This is the standard clinical approximation when direct
    # salivary melatonin measurement is unavailable.
    # Source: Lewy et al. (1999), Chronobiology International
    dlmo_estimate = biological_midnight - timedelta(hours=2)

    return {
        "biological_midnight":
            biological_midnight.isoformat(),

        "cbt_nadir_time":
            nadir_time.isoformat(),

        "dlmo_estimate":
            dlmo_estimate.isoformat(),

        "lowest_smoothed_temp":
            round(
                float(
                    nadir_row["smoothed_temp"]
                ),
                2
            ),

        "status": "calculated"
    }


def calculate_misalignment(
    behavioral_rows,
    biological_midnight
):

    if not behavioral_rows:

        return None

    sleep_logs = [
        row for row in behavioral_rows
        if row["event_type"] == "sleep_onset"
    ]

    if not sleep_logs:

        return None

    latest_sleep = sorted(
        sleep_logs,
        key=lambda x: x["timestamp"]
    )[-1]

    actual_sleep = pd.to_datetime(
        latest_sleep["timestamp"]
    )

    biological_midnight_dt = pd.to_datetime(
        biological_midnight
    )

    ideal_sleep_time = (
        biological_midnight_dt
        -
        timedelta(hours=2)
    )

    gap_hours = (
        actual_sleep
        -
        ideal_sleep_time
    ).total_seconds() / 3600

    if gap_hours > 12:

        gap_hours -= 24

    elif gap_hours < -12:

        gap_hours += 24

    return {
        "actual_sleep_time":
            actual_sleep.isoformat(),

        "ideal_sleep_time":
            ideal_sleep_time.isoformat(),

        "misalignment_hours":
            round(
                abs(
                    gap_hours
                ),
                2
            ),

        "status":
            (
                "aligned"
                if abs(gap_hours) < 1
                else "misaligned"
            )
    }


def calculate_glucose_stability(
    biochemical_rows
):

    glucose_values = []

    for row in biochemical_rows:

        glucose = None

        if (
            row.get(
                "glucose_value"
            ) is not None
        ):

            glucose = row.get(
                "glucose_value"
            )

        elif (
            row.get(
                "glucose_level"
            ) is not None
        ):

            glucose = row.get(
                "glucose_level"
            )

        if glucose is not None:

            glucose_values.append({

                "timestamp":
                    row.get(
                        "timestamp"
                    ),

                "glucose":
                    float(
                        glucose
                    )
            })

    if not glucose_values:

        return None

    df = pd.DataFrame(
        glucose_values
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="mixed",
        utc=True
    )

    df["glucose"] = pd.to_numeric(
        df["glucose"],
        errors="coerce"
    )

    avg_glucose = round(
        float(
            df["glucose"].mean()
        ),
        2
    )

    glucose_variability = round(
        float(
            df["glucose"].std()
        ),
        2
    )

    max_glucose = round(
        float(
            df["glucose"].max()
        ),
        2
    )

    if glucose_variability < 10:

        stability_status = "stable"

    elif glucose_variability < 20:

        stability_status = "moderate_variability"

    else:

        stability_status = "unstable"

    return {
        "average_glucose":
            avg_glucose,

        "glucose_variability":
            glucose_variability,

        "max_glucose":
            max_glucose,

        "status":
            stability_status
    }


def calculate_glucose_stability_from_override(
    glucose_override
):

    if not glucose_override:

        return None

    avg_glucose = glucose_override.get(
        "avg_glucose"
    )

    max_glucose = glucose_override.get(
        "max_glucose"
    )

    glucose_variability = glucose_override.get(
        "glucose_variability",
        0
    )

    if avg_glucose is None:

        return None

    if glucose_variability < 10:

        stability_status = "stable"

    elif glucose_variability < 20:

        stability_status = "moderate_variability"

    else:

        stability_status = "unstable"

    return {
        "average_glucose":
            round(
                float(avg_glucose),
                2
            ),

        "glucose_variability":
            round(
                float(glucose_variability),
                2
            ),

        "max_glucose":
            round(
                float(
                    max_glucose
                    or
                    avg_glucose
                ),
                2
            ),

        "status":
            stability_status
    }


def generate_zeitgebers(
    circadian_phase,
    misalignment_analysis,
    metabolic_analysis
):

    interventions = []

    if misalignment_analysis:

        if misalignment_analysis[
            "misalignment_hours"
        ] > 2:

            interventions.append({
                "type":
                    "light_exposure",

                "priority":
                    "high",

                "message":
                    (
                        "Get 15 minutes of outdoor light "
                        "within 30 minutes of waking."
                    )
            })

            interventions.append({
                "type":
                    "sleep_timing",

                "priority":
                    "high",

                "message":
                    (
                        "Shift bedtime earlier gradually "
                        "by 30 minutes tonight."
                    )
            })

    if metabolic_analysis:

        if metabolic_analysis[
            "max_glucose"
        ] > 130:

            interventions.append({
                "type":
                    "nutrition",

                "priority":
                    "medium",

                "message":
                    (
                        "Avoid late-night carbohydrates "
                        "to reduce nocturnal glucose spikes."
                    )
            })

        if metabolic_analysis[
            "glucose_variability"
        ] > 10:

            interventions.append({
                "type":
                    "meal_timing",

                "priority":
                    "medium",

                "message":
                    (
                        "Maintain consistent meal timing "
                        "to improve glucose stability."
                    )
            })

    return interventions


def calculate_user_digital_twin(
    user,
    physiological_rows,
    behavioral_rows,
    biochemical_rows,
    glucose_override=None
):

    phase_data = calculate_biological_midnight(
        physiological_rows
    )

    # Guard: new users have no physiological_rows yet.
    # Provide a fallback phase so the rest of the pipeline
    # can still run and save a snapshot for this user.
    if phase_data is None:

        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)

        # Default biological midnight: 3 AM UTC as a neutral starting point
        default_midnight = now.replace(
            hour=3, minute=0, second=0, microsecond=0
        )

        phase_data = {
            "biological_midnight":
                default_midnight.isoformat(),

            "cbt_nadir_time":
                now.replace(
                    hour=6, minute=0, second=0, microsecond=0
                ).isoformat(),

            # DLMO estimate: 2h before biological midnight
            "dlmo_estimate":
                now.replace(
                    hour=1, minute=0, second=0, microsecond=0
                ).isoformat(),

            "lowest_smoothed_temp":
                None,

            "status":
                "estimated_no_physiological_data"
        }

    misalignment = calculate_misalignment(
        behavioral_rows,
        phase_data["biological_midnight"]
    )

    glucose_analysis = None

    if glucose_override:

        glucose_analysis = (
            calculate_glucose_stability_from_override(
                glucose_override
            )
        )

    if glucose_analysis is None:

        glucose_analysis = calculate_glucose_stability(
            biochemical_rows
        )

    zeitgebers = generate_zeitgebers(
        phase_data,
        misalignment,
        glucose_analysis
    )

    return {
        "user_id":
            user["id"],

        "chronotype":
            user.get(
                "chronotype"
            ),

        "circadian_phase":
            phase_data,

        "misalignment_analysis":
            misalignment,

        "metabolic_analysis":
            glucose_analysis,

        "zeitgebers":
            zeitgebers,

        "status":
            "digital_twin_calculated"
    }
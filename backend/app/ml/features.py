import pandas as pd


def build_feature_vector(
    physiological_rows,
    biochemical_rows,
    behavioral_rows
):

    features = {}

    # PHYSIOLOGICAL FEATURES

    if physiological_rows:

        phys_df = pd.DataFrame(
            physiological_rows
        )

        phys_df["hrv"] = pd.to_numeric(
            phys_df["hrv"],
            errors="coerce"
        )

        phys_df["resting_heart_rate"] = pd.to_numeric(
            phys_df["resting_heart_rate"],
            errors="coerce"
        )

        phys_df["core_body_temp"] = pd.to_numeric(
            phys_df["core_body_temp"],
            errors="coerce"
        )

        features["avg_hrv"] = round(
            phys_df["hrv"].mean(),
            2
        )

        features["hrv_std"] = round(
            phys_df["hrv"].std(),
            2
        )

        features["avg_rhr"] = round(
            phys_df["resting_heart_rate"].mean(),
            2
        )

        features["avg_cbt"] = round(
            phys_df["core_body_temp"].mean(),
            2
        )

    # BIOCHEMICAL FEATURES

    if biochemical_rows:

        bio_df = pd.DataFrame(
            biochemical_rows
        )

        glucose_values = []

        for _, row in bio_df.iterrows():

            glucose = None

            if (
                "glucose_value" in bio_df.columns
                and
                pd.notna(
                    row.get(
                        "glucose_value"
                    )
                )
            ):

                glucose = row.get(
                    "glucose_value"
                )

            elif (
                "glucose_level" in bio_df.columns
                and
                pd.notna(
                    row.get(
                        "glucose_level"
                    )
                )
            ):

                glucose = row.get(
                    "glucose_level"
                )

            if glucose is not None:

                glucose_values.append(
                    float(
                        glucose
                    )
                )

        if glucose_values:

            glucose_series = pd.Series(
                glucose_values
            )

            features["avg_glucose"] = round(
                glucose_series.mean(),
                2
            )

            features["glucose_std"] = round(
                glucose_series.std(),
                2
            )

            features["max_glucose"] = round(
                glucose_series.max(),
                2
            )

    # BEHAVIORAL FEATURES

    if behavioral_rows:

        sleep_logs = [
            row for row in behavioral_rows
            if row["event_type"] == "sleep_onset"
        ]

        meal_logs = [
            row for row in behavioral_rows
            if row["event_type"] == "meal"
        ]

        features["sleep_log_count"] = len(
            sleep_logs
        )

        features["meal_log_count"] = len(
            meal_logs
        )

    return features
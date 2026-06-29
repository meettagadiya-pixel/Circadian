import pandas as pd


def detect_physiological_anomalies(
    snapshot_rows
):

    if len(snapshot_rows) < 5:
        return {
            "status": "not_enough_data"
        }

    df = pd.DataFrame(snapshot_rows)

    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )

    df = df.sort_values("created_at")

    alerts = []

    # -------------------------
    # HRV trend
    # -------------------------

    hrv_values = (
        df["avg_hrv"]
        .astype(float)
        .tolist()
    )

    if hrv_values[-1] < (
        sum(hrv_values[:-1])
        / len(hrv_values[:-1])
    ) * 0.85:

        alerts.append({
            "type": "hrv_decline",
            "severity": "medium",
            "message":
                "HRV has declined significantly."
        })

    # -------------------------
    # Glucose trend
    # -------------------------

    glucose_values = (
        df["avg_glucose"]
        .astype(float)
        .tolist()
    )

    if glucose_values[-1] > (
        sum(glucose_values[:-1])
        / len(glucose_values[:-1])
    ) * 1.10:

        alerts.append({
            "type": "glucose_elevation",
            "severity": "medium",
            "message":
                "Average glucose is trending upward."
        })

    # -------------------------
    # Fatigue trend
    # -------------------------

    fatigue_values = (
        df["fatigue_prediction"]
        .astype(float)
        .tolist()
    )

    if fatigue_values[-1] > (
        sum(fatigue_values[:-1])
        / len(fatigue_values[:-1])
    ):

        alerts.append({
            "type": "fatigue_risk",
            "severity": "high",
            "message":
                "Fatigue prediction is worsening."
        })

    if not alerts:

        return {
            "status": "stable",
            "alerts": []
        }

    return {
        "status": "anomalies_detected",
        "alerts": alerts
    }
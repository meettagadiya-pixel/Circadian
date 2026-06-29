def calculate_risk_state(
    anomaly_analysis,
    fatigue_prediction,
    misalignment_hours,
    glucose_variability
):
    """
    Circadian Stress Index (0-100)

    A composite indicator of circadian disruption severity.
    NOT a clinical risk score — intended as a longitudinal
    tracking metric for behavioural feedback.

    Component weights based on circadian disruption research:
      - Misalignment (50%): strongest published predictor of
        circadian-related health outcomes (Roenneberg et al., 2012)
      - HRV-derived fatigue (30%): autonomic nervous system
        suppression correlates with circadian strain
        (Firstbeat Technologies, 2014)
      - Glucose variability (20%): metabolic circadian disruption
        marker (Scheer et al., 2009 — PNAS)

    Anomaly penalties are additive but capped so a single
    anomaly cannot dominate the overall index.
    """

    # ─────────────────────────────────────────────────
    # MISALIGNMENT COMPONENT (0-50 points)
    # 8h misalignment = maximum disruption (50 points)
    # Linear scale: each hour = 6.25 points
    # ─────────────────────────────────────────────────

    misalignment_component = min(
        50,
        (misalignment_hours / 8) * 50
    )

    # ─────────────────────────────────────────────────
    # FATIGUE COMPONENT (0-30 points)
    # fatigue_prediction is 1-5 scale
    # 1 = low (6 pts), 5 = severe (30 pts)
    # ─────────────────────────────────────────────────

    fatigue_component = min(
        30,
        ((fatigue_prediction - 1) / 4) * 30
    )

    # ─────────────────────────────────────────────────
    # GLUCOSE VARIABILITY COMPONENT (0-20 points)
    # < 10% = stable (0 pts)
    # 10-20% = elevated (10 pts)
    # > 20% = high variability (20 pts)
    # ─────────────────────────────────────────────────

    if glucose_variability >= 20:
        glucose_component = 20
    elif glucose_variability >= 10:
        glucose_component = 10
    else:
        glucose_component = 0

    # ─────────────────────────────────────────────────
    # BASE INDEX
    # ─────────────────────────────────────────────────

    index = (
        misalignment_component
        + fatigue_component
        + glucose_component
    )

    # ─────────────────────────────────────────────────
    # ANOMALY PENALTY (max +10 points total)
    # Capped so anomalies cannot dominate the index
    # ─────────────────────────────────────────────────

    anomaly_penalty = 0

    if anomaly_analysis and anomaly_analysis.get(
        "status"
    ) == "anomalies_detected":

        alerts = anomaly_analysis.get("alerts", [])

        for alert in alerts:

            severity = alert.get("severity")

            if severity == "medium":
                anomaly_penalty += 3

            elif severity == "high":
                anomaly_penalty += 6

        anomaly_penalty = min(10, anomaly_penalty)

    index = min(100, round(index + anomaly_penalty))

    # ─────────────────────────────────────────────────
    # CLASSIFICATION
    # Thresholds aligned with misalignment severity:
    # < 25  = low     (< ~2h misalignment equivalent)
    # 25-50 = moderate (2-4h misalignment equivalent)
    # 50-75 = high    (4-6h misalignment equivalent)
    # > 75  = critical (> 6h misalignment equivalent)
    # ─────────────────────────────────────────────────

    if index < 25:
        state = "low"
    elif index < 50:
        state = "moderate"
    elif index < 75:
        state = "high"
    else:
        state = "critical"

    return {
        "risk_score":   index,
        "risk_state":   state,
        "risk_label":   "Circadian Stress Index",
        "components": {
            "misalignment": round(misalignment_component, 1),
            "fatigue":      round(fatigue_component, 1),
            "glucose":      round(glucose_component, 1),
            "anomalies":    anomaly_penalty
        }
    }
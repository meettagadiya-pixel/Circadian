def generate_training_labels(features):

    labels = {}

    # FATIGUE RISK
 

    fatigue_score = 0

    if features.get("avg_hrv", 100) < 45:
        fatigue_score += 2

    if features.get("avg_rhr", 0) > 72:
        fatigue_score += 2

    if features.get("glucose_std", 0) > 15:
        fatigue_score += 1

    labels["fatigue_risk"] = fatigue_score

    # CIRCADIAN INSTABILITY
  

    circadian_score = 0

    if features.get("sleep_log_count", 0) < 5:
        circadian_score += 2

    if features.get("avg_cbt", 0) > 36.9:
        circadian_score += 1

    labels["circadian_disruption_risk"] = circadian_score


    # METABOLIC INSTABILITY


    metabolic_score = 0

    if features.get("max_glucose", 0) > 130:
        metabolic_score += 2

    if features.get("glucose_std", 0) > 12:
        metabolic_score += 2

    labels["metabolic_risk"] = metabolic_score

    return labels
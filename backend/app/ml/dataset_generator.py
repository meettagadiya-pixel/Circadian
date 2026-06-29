import random
import pandas as pd


def generate_synthetic_dataset(num_samples=500):

    rows = []

    for _ in range(num_samples):

        avg_hrv = round(
            random.uniform(25, 80),
            2
        )

        avg_rhr = round(
            random.uniform(55, 90),
            2
        )

        avg_cbt = round(
            random.uniform(36.0, 37.3),
            2
        )

        avg_glucose = round(
            random.uniform(80, 130),
            2
        )

        glucose_std = round(
            random.uniform(5, 30),
            2
        )

        max_glucose = round(
            random.uniform(100, 220),
            2
        )

        sleep_log_count = random.randint(2, 10)

        meal_log_count = random.randint(2, 12)

  
        # LABEL GENERATION
   

        fatigue_risk = 0

        if avg_hrv < 40:
            fatigue_risk += 2

        if avg_rhr > 75:
            fatigue_risk += 2

        if glucose_std > 18:
            fatigue_risk += 1

        metabolic_risk = 0

        if max_glucose > 160:
            metabolic_risk += 2

        if glucose_std > 15:
            metabolic_risk += 2

        circadian_risk = 0

        if sleep_log_count < 5:
            circadian_risk += 2

        if avg_cbt > 36.9:
            circadian_risk += 1

        rows.append({
            "avg_hrv": avg_hrv,
            "avg_rhr": avg_rhr,
            "avg_cbt": avg_cbt,
            "avg_glucose": avg_glucose,
            "glucose_std": glucose_std,
            "max_glucose": max_glucose,
            "sleep_log_count": sleep_log_count,
            "meal_log_count": meal_log_count,
            "fatigue_risk": fatigue_risk,
            "metabolic_risk": metabolic_risk,
            "circadian_risk": circadian_risk
        })

    return pd.DataFrame(rows)
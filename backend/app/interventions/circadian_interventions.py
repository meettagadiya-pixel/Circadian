from datetime import datetime, timezone
from dateutil.parser import parse


def _fmt_time(iso_str):
    """Format ISO timestamp to readable HH:MM AM/PM"""
    if not iso_str:
        return None
    try:
        dt = parse(iso_str)
        return dt.strftime("%-I:%M %p")
    except Exception:
        return None


def _misalignment_label(hours):
    if hours < 1:
        return "minimal"
    if hours < 2:
        return "mild"
    if hours < 3.5:
        return "moderate"
    if hours < 5:
        return "significant"
    return "severe"


def _urgency_prefix(misalignment_hours, risk_state):
    if risk_state == "high" or misalignment_hours >= 5:
        return "Critical"
    if misalignment_hours >= 3:
        return "Important"
    return "Recommended"


def generate_circadian_interventions(
    misalignment,
    circadian_analysis,
    environmental=None,
    circadian_phase=None,
    metabolic_analysis=None,
    light_exposure_analysis=None,
    adherence=None,
    risk_state="moderate"
):
    interventions = []

    # ─────────────────────────────────────────
    # Pull all available real values
    # ─────────────────────────────────────────
    misalignment_score = misalignment.get("misalignment_score", 0) if misalignment else 0
    consistency_score = misalignment.get("consistency_score", 1) if misalignment else 1
    avg_midpoint = misalignment.get("avg_midpoint_hour", 0) if misalignment else 0
    misalignment_hours = misalignment.get("misalignment_hours", misalignment_score) if misalignment else misalignment_score
    actual_sleep_time = misalignment.get("actual_sleep_time") if misalignment else None
    ideal_sleep_time = misalignment.get("ideal_sleep_time") if misalignment else None

    bio_midnight = circadian_phase.get("biological_midnight") if circadian_phase else None
    cbt_nadir = circadian_phase.get("cbt_nadir_time") if circadian_phase else None

    sunrise = environmental.get("sunrise") if environmental else None
    sunset = environmental.get("sunset") if environmental else None
    uvi = environmental.get("uvi") if environmental else None
    clouds = environmental.get("clouds") if environmental else None

    avg_glucose = metabolic_analysis.get("avg_glucose") if metabolic_analysis else None
    max_glucose = metabolic_analysis.get("max_glucose") if metabolic_analysis else None
    glucose_variability = metabolic_analysis.get("glucose_variability") if metabolic_analysis else None

    bright_events = light_exposure_analysis.get("bright_light_events", 0) if light_exposure_analysis else 0
    night_events = light_exposure_analysis.get("night_light_events", 0) if light_exposure_analysis else 0

    meal_adherence = adherence.get("meal_adherence", 0) if adherence else 0
    exercise_adherence = adherence.get("exercise_adherence", 0) if adherence else 0
    sleep_adherence = adherence.get("sleep_adherence", 0) if adherence else 0

    label = _misalignment_label(misalignment_hours)
    prefix = _urgency_prefix(misalignment_hours, risk_state)

    bio_midnight_fmt = _fmt_time(bio_midnight)
    sunrise_fmt = _fmt_time(sunrise)
    sunset_fmt = _fmt_time(sunset)
    actual_sleep_fmt = _fmt_time(actual_sleep_time)
    ideal_sleep_fmt = _fmt_time(ideal_sleep_time)
    cbt_fmt = _fmt_time(cbt_nadir)

    # ─────────────────────────────────────────
    # LIGHT EXPOSURE — based on misalignment + actual light data
    # ─────────────────────────────────────────
    if misalignment_score > 0.7 or bright_events == 0:

        if sunrise_fmt and misalignment_hours >= 2:
            msg = (
                f"{prefix}: Your biological clock is delayed by "
                f"{misalignment_hours:.1f}h. "
                f"Get outdoor light within 30 minutes of waking — "
                f"sunrise today is {sunrise_fmt}. "
                f"Morning light is your strongest clock-resetting signal."
            )
        elif bright_events == 0 and sunrise_fmt:
            msg = (
                f"No bright-light exposure detected today. "
                f"Sunrise was {sunrise_fmt} — even 10 minutes outside "
                f"now will measurably shift your circadian phase forward."
            )
        elif uvi is not None and uvi < 2 and clouds and clouds > 70:
            msg = (
                f"Cloud cover is {clouds}% and UV is low ({uvi:.1f}). "
                f"Natural light is weak today — use a bright indoor light "
                f"(>1000 lux) for at least 20 minutes this morning "
                f"to compensate."
            )
        else:
            msg = (
                f"Your circadian rhythm shows {label} misalignment. "
                f"Prioritise outdoor light exposure early in your biological day."
            )

        interventions.append({
            "type": "light_exposure",
            "priority": "high" if misalignment_hours > 2 else "medium",
            "message": msg
        })

    # ─────────────────────────────────────────
    # EVENING LIGHT — night light detected
    # ─────────────────────────────────────────
    if night_events > 0 and sunset_fmt:
        interventions.append({
            "type": "light_exposure",
            "priority": "high",
            "message": (
                f"{night_events} bright-light event(s) detected near "
                f"your biological night. After {sunset_fmt}, switch to "
                f"dim warm lighting and enable night mode on all screens. "
                f"Evening light is delaying your clock further."
            )
        })

    # ─────────────────────────────────────────
    # SLEEP TIMING — uses actual vs ideal times
    # ─────────────────────────────────────────
    if consistency_score < 0.5:

        if actual_sleep_fmt and ideal_sleep_fmt and bio_midnight_fmt:
            msg = (
                f"Last night you slept at {actual_sleep_fmt} — "
                f"your biological ideal is {ideal_sleep_fmt} "
                f"(2h before biological midnight at {bio_midnight_fmt}). "
                f"That is a {misalignment_hours:.1f}h gap. "
                f"Shift bedtime 20 minutes earlier tonight to begin recovery."
            )
        elif bio_midnight_fmt:
            msg = (
                f"Your sleep timing is inconsistent. "
                f"Your biological midnight is {bio_midnight_fmt} — "
                f"aim to be asleep by "
                f"{ideal_sleep_fmt or '2 hours before that'}. "
                f"Fix wake time first: set an alarm for the same time "
                f"every day for 7 days."
            )
        else:
            msg = (
                f"Sleep schedule is irregular with {label} circadian misalignment. "
                f"Maintain a fixed wake time within ±15 minutes daily — "
                f"this is more powerful than fixing sleep time."
            )

        interventions.append({
            "type": "sleep_timing",
            "priority": "high",
            "message": msg
        })

    # ─────────────────────────────────────────
    # PHASE DELAY — biological night is shifted late
    # ─────────────────────────────────────────
    if avg_midpoint > 3 and cbt_fmt:
        interventions.append({
            "type": "sleep_timing",
            "priority": "medium",
            "message": (
                f"Your core body temperature nadir (CBT) is at {cbt_fmt} — "
                f"later than the typical 4-5 AM, indicating a delayed phase. "
                f"Move your morning light window earlier each day to gradually "
                f"pull your clock forward. Avoid naps after 3 PM."
            )
        })
    elif avg_midpoint > 3:
        interventions.append({
            "type": "sleep_timing",
            "priority": "medium",
            "message": (
                f"Your biological night is shifted approximately "
                f"{avg_midpoint:.1f}h later than the solar day. "
                f"Morning light and consistent wake times are the "
                f"most effective tools to advance your phase."
            )
        })

    # ─────────────────────────────────────────
    # GLUCOSE / NUTRITION
    # ─────────────────────────────────────────
    if max_glucose is not None and max_glucose > 130:
        msg = (
            f"Peak glucose reached {max_glucose:.0f} mg/dL — "
            f"above the 130 mg/dL nocturnal threshold. "
        )
        if meal_adherence < 0.5:
            msg += (
                f"Your meal timing adherence is {meal_adherence*100:.0f}%. "
                f"Eating close to biological night drives these spikes. "
                f"Stop eating 3 hours before {bio_midnight_fmt or 'biological midnight'}."
            )
        else:
            msg += (
                f"Try reducing refined carbohydrates at your last meal "
                f"and moving dinner 30 minutes earlier tonight."
            )
        interventions.append({
            "type": "nutrition",
            "priority": "high" if max_glucose > 150 else "medium",
            "message": msg
        })

    elif glucose_variability is not None and glucose_variability > 10:
        interventions.append({
            "type": "nutrition",
            "priority": "medium",
            "message": (
                f"Glucose variability is {glucose_variability:.1f}% — "
                f"elevated, which indicates inconsistent meal timing. "
                f"Eating at the same times each day relative to your "
                f"biological clock reduces this by up to 40%."
            )
        })

    # ─────────────────────────────────────────
    # RECOVERY — uses HRV-derived recovery score
    # ─────────────────────────────────────────
    recovery_scores = [
        item.get("recovery_score", 0)
        for item in circadian_analysis
    ] if circadian_analysis else []

    if recovery_scores:
        avg_recovery = sum(recovery_scores) / len(recovery_scores)

        if avg_recovery < 0.45:
            msg = (
                f"Recovery score is {avg_recovery*100:.0f}% — "
                f"below the 45% threshold. "
            )
            if exercise_adherence < 0.5:
                msg += (
                    f"Late or high-intensity exercise is likely contributing. "
                    f"Shift workouts to before {sunset_fmt or 'sunset'} "
                    f"and reduce intensity tonight."
                )
            else:
                msg += (
                    f"Prioritise 7-9 hours of uninterrupted sleep "
                    f"and avoid alcohol, which suppresses recovery by up to 25%."
                )
            interventions.append({
                "type": "recovery",
                "priority": "medium",
                "message": msg
            })

    # ─────────────────────────────────────────
    # MAINTENANCE — only if truly nothing is wrong
    # ─────────────────────────────────────────
    if not interventions:
        if bio_midnight_fmt:
            interventions.append({
                "type": "maintenance",
                "priority": "low",
                "message": (
                    f"Your circadian rhythm is well regulated. "
                    f"Biological midnight is stable at {bio_midnight_fmt}. "
                    f"Continue morning light exposure and consistent "
                    f"meal timing to maintain alignment."
                )
            })
        else:
            interventions.append({
                "type": "maintenance",
                "priority": "low",
                "message": (
                    "Circadian timing appears stable. "
                    "Maintain current light exposure, meal timing, "
                    "and sleep schedule."
                )
            })

    return interventions

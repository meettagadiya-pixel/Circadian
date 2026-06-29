from dateutil.parser import parse


def _fmt_time(iso_str):
    if not iso_str:
        return None
    try:
        dt = parse(iso_str)
        return dt.strftime("%-I:%M %p")
    except Exception:
        return None


def generate_contextual_interventions(
    meal_timing,
    exercise_timing,
    misalignment,
    recovery_score,
    light_exposure_analysis=None,
    circadian_phase=None,
    environmental=None,
    adherence=None
):
    interventions = []

    # Pull real values
    misalignment_hours = (
        misalignment.get("misalignment_hours",
            misalignment.get("misalignment_score", 0))
        if misalignment else 0
    )
    actual_sleep_fmt = _fmt_time(
        misalignment.get("actual_sleep_time") if misalignment else None
    )
    ideal_sleep_fmt = _fmt_time(
        misalignment.get("ideal_sleep_time") if misalignment else None
    )

    bio_midnight = circadian_phase.get("biological_midnight") if circadian_phase else None
    bio_midnight_fmt = _fmt_time(bio_midnight)

    sunrise_fmt = _fmt_time(environmental.get("sunrise") if environmental else None)
    sunset_fmt = _fmt_time(environmental.get("sunset") if environmental else None)
    uvi = environmental.get("uvi") if environmental else None
    clouds = environmental.get("clouds") if environmental else None

    meal_last_time = meal_timing.get("last_meal_time") if meal_timing else None
    meal_last_fmt = _fmt_time(meal_last_time)
    meal_hours_before_midnight = meal_timing.get("hours_before_midnight") if meal_timing else None

    exercise_last_time = exercise_timing.get("last_exercise_time") if exercise_timing else None
    exercise_last_fmt = _fmt_time(exercise_last_time)
    exercise_hours_before_midnight = exercise_timing.get("hours_before_midnight") if exercise_timing else None

    meal_score = adherence.get("meal_adherence", 0) if adherence else 0
    exercise_score = adherence.get("exercise_adherence", 0) if adherence else 0
    sleep_score = adherence.get("sleep_adherence", 0) if adherence else 0

    bright_events = light_exposure_analysis.get("bright_light_events", 0) if light_exposure_analysis else 0
    night_events = light_exposure_analysis.get("night_light_events", 0) if light_exposure_analysis else 0
    avg_lux = light_exposure_analysis.get("avg_lux") if light_exposure_analysis else None

    # ─────────────────────────────────────────
    # LATE MEAL
    # ─────────────────────────────────────────
    if meal_timing and meal_timing.get("status") == "late_eating_pattern":

        if meal_last_fmt and meal_hours_before_midnight is not None and bio_midnight_fmt:
            msg = (
                f"Last meal detected at {meal_last_fmt} — only "
                f"{abs(meal_hours_before_midnight):.1f}h before biological midnight "
                f"({bio_midnight_fmt}). "
                f"Late eating activates peripheral clocks in the liver and gut, "
                f"worsening misalignment. "
                f"Move your last meal to at least 3h before {bio_midnight_fmt}."
            )
        elif bio_midnight_fmt:
            msg = (
                f"Late-night eating pattern detected near biological midnight "
                f"({bio_midnight_fmt}). "
                f"Stop food intake 3 hours before your biological night begins. "
                f"Even shifting dinner 30 minutes earlier has measurable impact."
            )
        else:
            msg = (
                "Late-night eating detected near biological night. "
                "Avoid heavy carbohydrates after 9 PM. "
                "Time-restricted eating aligned to your clock improves both "
                "sleep quality and glucose stability."
            )

        interventions.append({
            "type": "nutrition",
            "priority": "high",
            "message": msg
        })

    # ─────────────────────────────────────────
    # LATE EXERCISE
    # ─────────────────────────────────────────
    if exercise_timing and exercise_timing.get("status") == "late_exercise_pattern":

        if exercise_last_fmt and exercise_hours_before_midnight is not None and bio_midnight_fmt:
            msg = (
                f"Exercise session detected at {exercise_last_fmt} — "
                f"{abs(exercise_hours_before_midnight):.1f}h before biological midnight. "
                f"Intense exercise within 3h of biological night raises core "
                f"temperature and cortisol, delaying sleep onset by 30-90 minutes. "
                f"Shift workouts to before {sunset_fmt or '6 PM'} where possible."
            )
        elif bio_midnight_fmt:
            msg = (
                f"Late exercise detected near biological midnight ({bio_midnight_fmt}). "
                f"Move intense workouts at least 4 hours earlier. "
                f"Light stretching or walking in the evening is fine."
            )
        else:
            msg = (
                "Exercise sessions are occurring too close to biological night. "
                "Shift intense workouts earlier in the day to avoid "
                "disrupting your sleep onset and circadian rhythm."
            )

        interventions.append({
            "type": "exercise_timing",
            "priority": "high",
            "message": msg
        })

    # ─────────────────────────────────────────
    # CIRCADIAN MISALIGNMENT
    # ─────────────────────────────────────────
    if misalignment_hours > 0.7:

        if actual_sleep_fmt and ideal_sleep_fmt:
            msg = (
                f"Sleep occurred at {actual_sleep_fmt} vs your biological ideal "
                f"of {ideal_sleep_fmt} — a {misalignment_hours:.1f}h gap. "
                f"The most effective reset: set a fixed wake time and hold it "
                f"regardless of when you fall asleep. After 5-7 days your "
                f"sleep onset will follow naturally."
            )
        elif bio_midnight_fmt:
            msg = (
                f"Circadian misalignment of {misalignment_hours:.1f}h detected. "
                f"Your biological midnight is {bio_midnight_fmt}. "
                f"A consistent wake time anchors your clock — "
                f"variation of more than 30 minutes undoes weekly progress."
            )
        else:
            msg = (
                f"Circadian instability detected ({misalignment_hours:.1f}h misalignment). "
                f"Maintain a fixed wake time within ±15 minutes daily. "
                f"This single habit has the highest evidence base for "
                f"resetting circadian timing."
            )

        interventions.append({
            "type": "sleep_schedule",
            "priority": "high",
            "message": msg
        })

    # ─────────────────────────────────────────
    # LIGHT EXPOSURE — contextual
    # ─────────────────────────────────────────
    if light_exposure_analysis:

        if bright_events == 0 and sunrise_fmt:
            if uvi is not None and clouds is not None:
                msg = (
                    f"No bright-light events recorded today. "
                    f"UV index is {uvi:.1f} with {clouds}% cloud cover — "
                    f"{'natural light is limited, ' if clouds > 70 else ''}"
                    f"aim for at least 15 minutes outside in the morning. "
                    f"Even overcast light (1000-5000 lux) is 10x stronger "
                    f"than indoor lighting for circadian signalling."
                )
            else:
                msg = (
                    f"No bright-light exposure detected. "
                    f"Get outdoor light exposure early in your biological day — "
                    f"ideally within 30 minutes of waking. "
                    f"This is the single most powerful zeitgeber for your clock."
                )
            interventions.append({
                "type": "light_exposure",
                "priority": "high",
                "message": msg
            })

        if night_events > 0 and sunset_fmt:
            msg = (
                f"{night_events} bright-light event(s) after {sunset_fmt}. "
                f"Evening light suppresses melatonin for 90-120 minutes, "
                f"delaying sleep onset regardless of how tired you feel. "
                f"Use f.lux, night mode, or dim amber lighting after sunset."
            )
            interventions.append({
                "type": "light_exposure",
                "priority": "high",
                "message": msg
            })

    # ─────────────────────────────────────────
    # LOW RECOVERY
    # ─────────────────────────────────────────
    hrv_pct = recovery_score * 100

    if recovery_score < 0.5:

        if exercise_score < 0.5 and sleep_score < 0.5:
            msg = (
                f"Recovery is at {hrv_pct:.0f}% — both sleep consistency "
                f"({sleep_score*100:.0f}%) and exercise timing "
                f"({exercise_score*100:.0f}%) are below threshold. "
                f"Tonight: no exercise, in bed by {ideal_sleep_fmt or 'your biological ideal'}, "
                f"and no screens after {sunset_fmt or 'sunset'}."
            )
        elif sleep_score < 0.5:
            msg = (
                f"Recovery at {hrv_pct:.0f}%. Sleep consistency "
                f"({sleep_score*100:.0f}%) is the primary driver. "
                f"Prioritise getting to bed closer to "
                f"{ideal_sleep_fmt or 'your biological ideal time'} tonight."
            )
        else:
            msg = (
                f"Recovery markers at {hrv_pct:.0f}% — below healthy threshold. "
                f"Reduce today's exercise intensity, avoid alcohol, "
                f"and aim for 8+ hours tonight."
            )

        interventions.append({
            "type": "recovery",
            "priority": "medium",
            "message": msg
        })

    return interventions

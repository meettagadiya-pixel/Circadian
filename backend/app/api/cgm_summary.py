from fastapi import APIRouter

from app.ingestion.unified_ingestion import (
    get_provider_user_id
)

from app.ingestion.junction_fetcher import (
    fetch_freestyle_libre_glucose
)

from app.ingestion.junction_parser import (
    extract_timeseries_values
)


router = APIRouter()


@router.get("/cgm-summary")
def cgm_summary(
    user_id: str
):

    provider_user_id = (
        get_provider_user_id(
            user_id
        )
    )

    response = fetch_freestyle_libre_glucose(
        provider_user_id
    )

    readings = extract_timeseries_values(
        response
    )

    if not readings:

        return {
            "status": "no_glucose_data",
            "user_id": user_id,
            "source": "junction_freestyle_libre"
        }

    converted_readings = []

    glucose_values = []

    for item in readings:

        mmol_value = item.get(
            "value"
        )

        if mmol_value is None:
            continue

        mgdl_value = round(
            float(mmol_value) * 18,
            2
        )

        glucose_values.append(
            mgdl_value
        )

        converted_readings.append({
            "timestamp":
                item.get(
                    "timestamp"
                ),

            "glucose_mmol_l":
                mmol_value,

            "glucose_mg_dl":
                mgdl_value,

            "source":
                "junction_freestyle_libre"
        })

    if not glucose_values:

        return {
            "status": "no_glucose_data",
            "user_id": user_id,
            "source": "junction_freestyle_libre"
        }

    avg_glucose = round(
        sum(glucose_values)
        /
        len(glucose_values),
        2
    )

    max_glucose = round(
        max(glucose_values),
        2
    )

    min_glucose = round(
        min(glucose_values),
        2
    )

    high_readings = len([
        value for value in glucose_values
        if value >= 140
    ])

    return {
        "status": "success",
        "user_id": user_id,
        "source": "junction_freestyle_libre",
        "unit": "mg/dL",
        "original_unit": "mmol/L",
        "reading_count": len(glucose_values),
        "avg_glucose": avg_glucose,
        "min_glucose": min_glucose,
        "max_glucose": max_glucose,
        "high_reading_count": high_readings,
        "latest_readings": converted_readings[-10:]
    }
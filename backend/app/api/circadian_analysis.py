from fastapi import APIRouter

from app.ingestion.junction_fetcher import (
    fetch_fitbit_sleep
)

from app.physiology.circadian import (
    estimate_circadian_phase
)
from app.physiology.misalignment import (
    calculate_misalignment
)
from app.interventions.circadian_interventions import (
    generate_circadian_interventions
)
from app.analytics.circadian_trends import (
    analyze_circadian_trends
)

router = APIRouter()


@router.get("/circadian-analysis")
def circadian_analysis():

    response = fetch_fitbit_sleep(
        "5c986070-4eae-457e-917b-5a2ba2713fc6"
    )

    sleep_data = (
        response["data"]
        .get("sleep", [])
    )

    analysis = []

    for item in sleep_data:

        analysis.append(
            estimate_circadian_phase(
                item
            )
        )

        misalignment = calculate_misalignment(
            analysis
        )

        interventions = (
            generate_circadian_interventions(
                misalignment,
                analysis
            )
        )

        trends = analyze_circadian_trends(
            analysis
        )

    return {

        "status":
            "success",

        "misalignment_analysis":
            misalignment,
    
        "trend_analysis":
            trends,
        
        "interventions":
            interventions,

        "circadian_analysis":
            analysis,
        
    }
from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from workers.physiology_worker import (
    run_physiology_pipeline
)

scheduler = BackgroundScheduler()


def start_scheduler():

    scheduler.add_job(
        run_physiology_pipeline,
        trigger="interval",
        minutes=1
    )

    scheduler.start()

    print(
        "Physiology scheduler started."
    )
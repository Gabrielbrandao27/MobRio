from app.tasks.celery_tasks import fetch_todays_buses

fetch_todays_buses.delay()
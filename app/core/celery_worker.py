from celery import Celery
from datetime import timedelta

celery_app = Celery(
    "worker",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://"
)

celery_app.conf.beat_schedule = {
    'fetch-bus-data-every-minute': {
        'task': 'celery_tasks.fetch_bus_data',
        'schedule': timedelta(minutes=1)
    },
}

# Importa as tasks para que o worker conheça
import app.tasks.celery_tasks as celery_tasks

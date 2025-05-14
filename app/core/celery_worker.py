from celery import Celery
from datetime import timedelta

app = Celery(
    "worker",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://"
)

app.conf.beat_schedule = {
    'fetch-bus-data-every-minute': {
        'task': 'app.tasks.celery_tasks.fetch_buses_every_minute',
        'schedule': timedelta(minutes=1)
    },
    'notify-users-about-bus-every-minute': {
        'task': 'app.tasks.celery_tasks.notify_users_about_bus',
        'schedule': timedelta(minutes=1)
    },
}

# Importa as tasks para que o worker conheça
import app.tasks.celery_tasks as celery_tasks
# celery -A app.core.celery_worker.app worker --beat --loglevel=info
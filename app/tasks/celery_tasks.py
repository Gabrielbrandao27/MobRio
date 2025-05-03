import json
import redis
import requests
from datetime import datetime, timedelta
from app.core.celery_worker import app

r = redis.Redis(host='localhost', port=6379, db=0)

@app.task
def fetch_buses_every_minute():
    now = datetime.now()
    open_time = (now - timedelta(minutes=1)).strftime("%Y-%m-%d+%H:%M:%S")
    close_time = now.strftime("%Y-%m-%d+%H:%M:%S")

    url = f"https://dados.mobilidade.rio/gps/sppo?dataInicial={open_time}&dataFinal={close_time}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        r.set('bus_struct', json.dumps(data))

        return data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


if __name__ == "__main__":

    print(fetch_buses_every_minute())
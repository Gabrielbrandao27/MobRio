import requests
from datetime import datetime, timedelta
from celery_worker import celery_app

@celery_app.task
def fetch_todays_buses():
    now = datetime.now()
    open_time = now.strftime("%Y-%m-%d+%H:%M:%S")
    close_time = (now + timedelta(minutes=1)).strftime("%Y-%m-%d+%H:%M:%S")

    url = f"https://dados.mobilidade.rio/gps/sppo?dataInicial={open_time}&dataFinal={close_time}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        bus_lines = set()
        for item in data:
            bus_lines.add(item['linha'])

        return list(bus_lines)
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


if __name__ == "__main__":

    print(fetch_todays_buses())
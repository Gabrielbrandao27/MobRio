import json
import redis
import requests
from datetime import datetime, timedelta
from db.db_manager import DBManager
from core.celery_worker import app
from utils.process_positions import process_live_positions
from utils.send_email import send_email

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


@app.task
def notify_users_about_bus():
    try:
        # Obter todos os usuários
        db = DBManager()
        users = db.fetch_all("SELECT id, email FROM users")
        db.close()

        for user in users:
            user_id = user["id"]
            user_email = user["email"]

            # Processar posições ao vivo para o usuário
            result = process_live_positions(user_id)

            if "error" in result:
                print(f"Erro ao processar posições para o usuário {user_id}: {result['error']}")
                continue

            live_positions = result["live_positions"]

            # Verificar se algum ônibus está a 10 minutos ou menos
            for position in live_positions:
                if position["tempo_chegada"] <= 10:
                    send_email(
                        to=user_email,
                        subject="Seu ônibus está chegando!",
                        body=f"O ônibus da linha {position['route_name']} está a {position['tempo_chegada']} minutos do seu ponto {position['stop_name']}."
                    )
                    print(f"E-mail enviado para {user_email} sobre a linha {position['route_name']}.")
    except Exception as e:
        print(f"Erro na task notify_users_about_bus: {e}")


if __name__ == "__main__":

    print(fetch_buses_every_minute())
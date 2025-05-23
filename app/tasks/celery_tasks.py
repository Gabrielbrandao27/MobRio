import json
import redis
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from db.db_manager import DBManager
from core.celery_worker import app
from utils.process_positions import process_live_positions
from utils.send_email import send_email

r = redis.Redis(host='redis', port=6379, db=0)

@app.task
def fetch_buses_every_minute():
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
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

            # Verificar se algum ônibus está a 10 minutos ou menos do horário de abertura do usuário
            for position in live_positions:
                now = datetime.now(ZoneInfo("America/Sao_Paulo"))
                if "tempo_chegada" not in position or position["tempo_chegada"] is None:
                    continue
                arrival_time = now + timedelta(minutes=position["tempo_chegada"])

                # Converter hora_abertura e hora_fechamento para objetos datetime.time, se necessário
                hora_abertura = datetime.strptime(position["hora_abertura"].split(".")[0], "%H:%M:%S").time() if isinstance(position["hora_abertura"], str) else position["hora_abertura"]
                hora_fechamento = datetime.strptime(position["hora_fechamento"].split(".")[0], "%H:%M:%S").time() if isinstance(position["hora_fechamento"], str) else position["hora_fechamento"]

                # Verificar se o horário de chegada está dentro do intervalo definido pelo usuário
                if hora_abertura <= arrival_time.time() <= hora_fechamento:
                    # Verificar se o ônibus está a 10 minutos ou menos da parada
                    if timedelta(minutes=position["tempo_chegada"]) <= timedelta(minutes=10):
                        # Enviar e-mail para o usuário
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
# MobRio

## Proposta:
Construir um web app que se alimenta minuto a minuto das posições dos ônibus do Rio de Janeiro, permita que o usuário cadastre um ônibus, ponto e janela de horário de partida e a partir desse cadastro gere um e-mail de notificação para o usuário sempre que algum ônibus dessa linha esteja a 10 minutos de chegar nessa localização dentro da faixa de horário estabelecida. Além disso, o aplicativo deve ter uma tela que mostra uma tabela de todos os ônibus da linha selecionada, sua velocidade e tempo até o local de partida do usuário.

- Desejável:
1. Utilizar docker
2. Na mesma tela da tabela, mostrar os ônibus da linha posicionados num mapa.

- Stack:
1. O backend deve ser desenvolvido utilizando FastAPI e o frontend deve ser desenvolvido utilizando React.
2. Sugestão: Utilizar a biblioteca celery para a obtenção periódica dos dados e o alerta para o usuário

- Instruções de Publicação:
1. O desafio deve ser acompanhado de instruções para instalação/execução, prints da tela do sistema e um vídeo de overview do código de aproximadamente 5 minutos (Sugestão: https://www.loom.com/)

- Referências Úteis:
1. Para calculo de tempo de viagem estimado: traveltime.com ou similar
2. Para renderizar o mapa: https://leafletjs.com/
3. API de posicionamento dos ônibus do Rio de Janeiro: https://dados.mobilidade.rio/gps/sppo?dataInicial=2024-01-29+15:40:00&dataFinal=2024-01-29+15:43:00


# Instruções para compilação

1. cd frontend -> npm run dev
2. cd app -> fastapi dev main.py
3. celery -A app.core.celery_worker.app worker --beat --loglevel=info

FROM python:3.12-slim

# Atualizar pacotes e instalar dependências necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Criar um usuário não root
RUN useradd -m appuser

WORKDIR /app

# Copiar o arquivo zipado para o contêiner
COPY db/bus_data.zip /app/db/bus_data.zip

# Descompactar o arquivo zipado
RUN unzip /app/db/bus_data.zip -d /app/db/ && \
    rm /app/db/bus_data.zip

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Alterar para o usuário não root
USER appuser

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
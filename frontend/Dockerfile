# Stage 1: Build
FROM node:22-alpine AS builder

WORKDIR /app

# Copiar apenas os arquivos necessários para instalar dependências
COPY package*.json ./
RUN npm install

# Copiar o restante do código e construir o projeto
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:22-alpine

WORKDIR /app

# Criar um usuário não root para segurança
RUN adduser -D appuser
USER appuser

# Copiar apenas os arquivos necessários para o ambiente de produção
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Expor a porta para o servidor de preview do Vite
EXPOSE 4173

# Comando para iniciar o servidor
CMD ["npm", "run", "preview", "--", "--host"]
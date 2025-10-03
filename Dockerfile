# Etapa 1: A Base
FROM python:3.11-slim

# Etapa 2: O Ambiente
WORKDIR /app

# Etapa 3: Copiando os Ingredientes
COPY api_backend/requirements.txt .

# Etapa 4: Instalando os Ingredientes
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiando o Código e o Conhecimento (CORRIGIDO)
COPY ./api_backend .
COPY ./base_conhecimento ./base_conhecimento

# Etapa 6: A Porta
EXPOSE 8080

# Etapa 7: O Comando Final
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

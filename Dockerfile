# ESTE É O CONTEÚDO CORRETO PARA O ARQUIVO /encontro-dagua-hub/Dockerfile

# Etapa 1: A Base
FROM python:3.11-slim

# Etapa 2: O Ambiente de Trabalho
WORKDIR /app

# Etapa 3: Copiando a Lista de Ingredientes
# Pega o requirements.txt de dentro da api_backend
COPY api_backend/requirements.txt .

# Etapa 4: Instalando os Ingredientes
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiando todo o código da API
# Copia TUDO que está dentro de 'api_backend' (incluindo 'main.py' e a subpasta 'base_conhecimento')
# para dentro da nossa "caixa" no diretório /app
COPY ./api_backend .

# Etapa 6: Copiando o Livro de Receitas dos Gems
COPY ./specs ./specs

# Etapa 7: Expondo a Porta que o Cloud Run vai usar
EXPOSE 8080

# Etapa 8: O Comando CORRETO para Ligar o Servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
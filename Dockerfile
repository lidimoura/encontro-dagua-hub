# Etapa 1: A Base - Começamos com uma imagem oficial e leve do Python
FROM python:3.11-slim

# Etapa 2: O Ambiente - Definimos onde nosso código vai morar dentro da "caixa"
WORKDIR /app

# Etapa 3: Copiando os Ingredientes - Copiamos primeiro a lista de requisitos
COPY api_backend/requirements.txt .

# Etapa 4: Instalando os Ingredientes - Instalamos todas as bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiando o Coração - Agora copiamos todo o código da nossa API
COPY ./api_backend .

# Etapa 6: A Porta - Dizemos ao mundo que nossa API vai "ouvir" na porta 8080
EXPOSE 8080

# Etapa 7: O Comando Final - A instrução para ligar o servidor quando a "caixa" iniciar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# Etapa 1: A Base
FROM python:3.11-slim

# Etapa 2: O Ambiente de Trabalho
WORKDIR /app

# Etapa 3: Copiando a Lista de Ingredientes
COPY requirements.txt .

# Etapa 4: Instalando os Ingredientes
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiando o código da interface
COPY app.py .

# Etapa 6: Expondo a Porta que o Cloud Run vai usar
EXPOSE 8080

# Etapa 7: O Comando para Ligar o Servidor Streamlit
# Importante: O Streamlit precisa rodar com essas flags para funcionar bem no Cloud Run
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false"]
# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Define variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes como o faiss-cpu.
# - apt-get update: Atualiza a lista de pacotes disponíveis.
# - apt-get install -y: Instala os pacotes sem pedir confirmação.
# - build-essential: Inclui compiladores C/C++ (g++).
# - libopenblas-dev: Dependência numérica para faiss.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libopenblas-dev && rm -rf /var/lib/apt/lists/*

# Copie o arquivo de dependências
COPY requirements.txt requirements.txt

# Instale as dependências (e remova o cache para manter a imagem pequena)
RUN pip install --no-cache-dir -r requirements.txt

# Copie os arquivos da aplicação para o contêiner
COPY main.py .
COPY base_conhecimento/ ./base_conhecimento/

# Comando para executar a aplicação quando o contêiner iniciar
# Isso vai executar o bloco `if __name__ == "__main__":` no seu main.py
CMD ["python", "main.py"]

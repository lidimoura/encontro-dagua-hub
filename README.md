<div align="center">

# Encontro d'água hub 
Onde tecnologia e sustentabilidade se encontram. Este repositório é o coração do nosso ecossistema de agentes de IA, construído com a filosofia de "reflorestar o digital".

</div>

<p align="center">
<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-blue" alt="Status do Projeto">
<img src="https://img.shields.io/badge/Linguagem-Python-3776AB?logo=python&logoColor=white" alt="Linguagem Principal">
<img src="https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white" alt="Backend">
<img src="https://img.shields.io/badge/Database-Supabase-3ECF8E?logo=supabase&logoColor=white" alt="Database">
<img src="https://img.shields.io/badge/AI-Google%20Gemini-8952FF?logo=google&logoColor=white" alt="IA Generativa">
<a href="https://www.google.com/search?q=LICENSE">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Licença">
</a>
</p>

<p align="center">
<a href="#-sobre-o-projeto">Sobre</a> •
<a href="#-arquitetura-do-hub">Arquitetura</a> •
<a href="#-tecnologias-utilizadas">Tecnologias</a> •
<a href="#-estrutura-do-repositório">Estrutura</a> •
<a href="#-como-começar">Como Começar</a> •
<a href="#-contribuição">Contribuição</a> •
<a href="#-licença">Licença</a> •
<a href="#-contato">Contato</a>
</p>

<h3 align= "center"> Sobre o Projeto </h3>
<div align= "center">Em um mundo digital que cresce exponencialmente, o Encontro D'Água Hub nasce com um propósito: criar tecnologia de forma sustentável. Assim como na natureza, onde nada se perde e tudo se transforma, nosso objetivo é construir um ecossistema de "Gems" (nossos agentes de IA) que sejam eficientes, que reaproveitem conhecimento e que não gerem "lixo digital".

Este projeto, inspirado no encontro das águas dos rios Negro e Solimões em Manaus, busca automatizar, otimizar e criar, mas sempre com a consciência do impacto e com a beleza da colaboração. </div>

<h3 align= "center"> Arquitetura do Hub </h3>
<div align= "center">Este projeto é um monorepo que centraliza todo o ecossistema de Gems. A arquitetura é baseada em três pilares principais:

O Cérebro (Backend API): Uma API em FastAPI que serve como o ponto central para invocar os Gems, orquestrando toda a lógica.

A Memória (RAG & Supabase): Nossos Gems evoluem através de:

RAG (Retrieval-Augmented Generation): Uma base de conhecimento com documentações que os Gems consultam para dar respostas contextualizadas.

Memória Persistente: Um "Diário de Logs" no Supabase que registra as interações, permitindo aprendizado contínuo.

O Rosto (Interface): Um painel de controle interativo para gerenciar e interagir com os Gems. </div>

<h3 align= "center"> Tecnologias Utilizadas </h3>
<div align= "center">Linguagem Principal: Python

Backend: FastAPI

IA Generativa: API do Google Gemini

Banco de Dados e memória: Supabase

Interface (Prototipagem): Streamlit/Lovable

Base de Conhecimento: LangChain / LlamaIndex

Hospedagem: Render

Versionamento: GIt & GitHub</div>

<h3 align= "center"> 📁 Estrutura do Repositório </h3>

```bash
/encontro-dagua-hub
  ├── 📂 api_backend/       # Código da API principal em FastAPI
  ├── 📂 assets/            # Imagens, logos e animações do projeto
  ├── 📂 interface/         # Código do frontend
  ├── 📂 knowledge_base/    # Documentos para o RAG
  ├── 📂 scripts/           # Scripts úteis e de automação
  ├── 📂 specs/             # O "DNA" de cada Gem (blueprints)
  ├── 📄 .gitignore        # Define o que o Git deve ignorar
  ├── 📄 LICENSE           # Licença MIT
  └── 📄 README.md         # Este arquivo :)
  ```

<h3 align= "center"> Como Começar </h3>
<div align= "center"> O projeto está em desenvolvimento ativo. Para configurar o ambiente localmente, siga os passos abaixo: </div>

``` bash

# 1. Clone o repositório
git clone https://github.com/lidimoura/encontro-dagua-hub.git

# 2. Navegue até o diretório do projeto
cd encontro-dagua-hub

# 3. Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows, use `.venv\Scripts\activate`

# 4. Instale as dependências (arquivo a ser criado)
pip install -r requirements.txt
```
<h3 align= "center"> 🤝 Contribuição </h3>
<div align= "center">No momento, este projeto está em fase inicial. Em breve, abriremos guias de contribuição para quem quiser se juntar a nós na missão de reflorestar o digital. Por enquanto, sinta-se à vontade para abrir uma issue com sugestões ou reportar bugs. </div>

<h3 align= "center">  Licença </h3>
<div align= "center">Este projeto é licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

<h3 align= "center">  Contato </h3>
<div align="center">
<p> Lídi Moura </p>

<a href="https://www.linkedin.com/in/lidimoura/">
<img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>
<a href="https://github.com/lidimoura">
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>
</div>

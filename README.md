<div align="center">

# Encontro d'água hub 
Onde tecnologia e sustentabilidade se encontram. Este repositório é o coração do nosso ecossistema de agentes de IA, construído com a filosofia de "reflorestar o digital".

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-778899" alt="Status do Projeto">
  <img src="https://img.shields.io/badge/Linguagem-Python-556B2F?logo=python&logoColor=white" alt="Linguagem Principal">
  <img src="https://img.shields.io/badge/Backend-FastAPI-556B2F?logo=fastapi&logoColor=white" alt="Backend">
  <img src="https://img.shields.io/badge/Database-Supabase-A0522D?logo=supabase&logoColor=white" alt="Database">
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-C46210?logo=google&logoColor=white" alt="IA Generativa">
  <a href="LICENSE">
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
<div align= "justify">
  
-   **Linguagem Principal:** ![Python](https://img.shields.io/badge/Python-556B2F?style=for-the-badge&logo=python&logoColor=white)
-   **Backend:** ![FastAPI](https://img.shields.io/badge/FastAPI-556B2F?style=for-the-badge&logo=fastapi&logoColor=white)
-   **IA Generativa:** ![Google Gemini](https://img.shields.io/badge/Google%20Gemini-C46210?style=for-the-badge&logo=google&logoColor=white)
-   **Banco de Dados & Memória:** ![Supabase](https://img.shields.io/badge/Supabase-A0522D?style=for-the-badge&logo=supabase&logoColor=white)
-   **Interface (Prototipagem):** ![Streamlit](https://img.shields.io/badge/Streamlit-C46210?style=for-the-badge&logo=streamlit&logoColor=white) & **Lovable**
-   **Base de Conhecimento (RAG):** ![LangChain](https://img.shields.io/badge/LangChain-556B2F?style=for-the-badge&logo=langchain&logoColor=white)
-   **Hospedagem:** ![Hostinger](https://img.shields.io/badge/Hostinger-A0522D?style=for-the-badge&logo=hostinger&logoColor=white)
-   **Versionamento:** ![Git](https://img.shields.io/badge/Git-778899?style=for-the-badge&logo=git&logoColor=white) & ![GitHub](https://img.shields.io/badge/GitHub-778899?style=for-the-badge&logo=github&logoColor=white)
-   **Automação (CI/CD):** ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-778899?style=for-the-badge&logo=githubactions&logoColor=white)</div>

<h3 align= "center"> 📁 Estrutura do Repositório </h3>

```bash
## 📁 Estrutura do Repositório

/encontro-dagua-hub
  ├── 📂 api_backend/
  │   ├── 📂 base_conhecimento/
  │   │   ├── 📄 stack_atual_v2.md
  │   │   └── ... (outros guias .md)
  │   ├── 📄 main.py
  │   └── 📄 requirements.txt
  ├── 📂 interface/
  │   └── 📄 app.py
  ├── 📂 specs/
  │   └── ... (todos os DNAs dos Gems .md)
  ├── 📂 fontes/
  │   └── ... (documentos de pesquisa para o NotebookLM)
  ├── 📂 prompts/
  │   └── ... (nossos prompts mestres salvos)
  ├── 📄 Dockerfile
  ├── 📄 requirements.txt      
  ├── 📄 README.md
  └── 📄 LICENSE  
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
<p align="center">
  **Lidi Moura**
  <br>
  <a href="https://www.linkedin.com/in/lidimoura/">
    <img src="https://img.shields.io/badge/LinkedIn-6699CC?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://github.com/lidimoura">
    <img src="https://img.shields.io/badge/GitHub-778899?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
</p>

<div align="center">

# Encontro d'água hub 🌀
Onde tecnologia e sustentabilidade se encontram. Este repositório é o coração do nosso ecossistema de agentes de IA, construído com a filosofia de "reflorestar o digital".

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Status-LANÇADO-28A745" alt="Status do Projeto">
  <img src="https://img.shields.io/badge/Linguagem-Python-556B2F?logo=python&logoColor=white" alt="Linguagem Principal">
  <img src="https://img.shields.io/badge/Backend-Streamlit-556B2F?logo=streamlit&logoColor=white" alt="Backend">
  <img src="https://img.shields.io/badge/Database-Supabase-A0522D?logo=supabase&logoColor=white" alt="Database">
  <img src="https://img.shields.io/badge/AI-OpenAI-000000?logo=openai&logoColor=white" alt="IA Generativa">
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
<div align= "center">Em um mundo digital que cresce exponencialmente, o Encontro D'Água Hub nasce com um propósito: criar tecnologia de forma sustentável. Assim como na natureza, onde nada se perde e tudo se transforma, nosso objetivo é construir um ecossistema de Agentes de IA que sejam eficientes, que reaproveitem conhecimento e que não gerem "lixo digital".

Este projeto, inspirado no encontro das águas dos rios Negro e Solimões em Manaus, busca automatizar, otimizar e criar, mas sempre com a consciência do impacto e com a beleza da colaboração. </div>

<h3 align= "center"> Arquitetura do Hub </h3>
<div align= "center">Este projeto agora opera na arquitetura **"Tudo-em-Um" (Monolítica Simples)**. Após o pivô estratégico, toda a lógica do Hub está consolidada em uma única aplicação Streamlit, eliminando a complexidade de microsserviços. A arquitetura é baseada em três pilares principais:

O Cérebro & Rosto: O arquivo `interface/app.py` no Streamlit Cloud concentra toda a lógica de execução e a interface de usuário.

A Inteligência (LLM & RAG): Utilizamos a API da **OpenAI** (GPT-3.5-Turbo) como motor principal, e **LangChain** para orquestrar o RAG (Retrieval-Augmented Generation) com a base de conhecimento.

A Memória Persistente: **Supabase** é o nosso banco de dados PostgreSQL que registra as interações (`chat_memory`), permitindo aprendizado contínuo e auditoria. </div>


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
  ├── 📂 interface/             <-- (O cérebro do hub)
  │   └── 📄 app.py
  ├── 📂 specs/                 <-- Contém todos os DNAs dos agentes especialistas (.md)
  ├── 📂 base_conhecimento/      <-- As bases de conhecimento (RAG) e guias do hub
  ├── 📄 requirements.txt
  ├── 📄 gemini.md              <-- Dossiê da evolução e processos do hub
  ├── 📄 README.md
  └── 📄 LICENSE  
 ```

<h3 align= "center"> Como Começar </h3>
<div align= "center"> O projeto está **LANÇADO** e rodando no Streamlit Cloud. Para configurar o ambiente localmente (caso necessário): </div>


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

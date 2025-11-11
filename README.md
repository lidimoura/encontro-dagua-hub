<div align="center">

# Encontro d'água Hub 🌀

Onde tecnologia e sustentabilidade se encontram. Este repositório é o coração do nosso ecossistema de agentes de IA, construído com a filosofia de "reflorestar o digital".

</div>

<p align="center">
    <img src="https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow" alt="Status do Projeto">
    <img src="https://img.shields.io/badge/Branch_Principal-main-blue" alt="Branch Principal">
    <img src="https://img.shields.io/badge/Linguagem-Python-556B2F?logo=python&logoColor=white" alt="Linguagem Principal">
    <img src="https://img.shields.io/badge/Interface-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Interface">
    <img src="https://img.shields.io/badge/Database-Supabase-3ECF8E?logo=supabase&logoColor=white" alt="Database">
    <img src="https://img.shields.io/badge/AI-OpenAI_&_LangChain-000000?logo=openai&logoColor=white" alt="IA Generativa">
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

## Sobre o Projeto

Em um mundo digital que cresce exponencialmente, o Encontro D'Água Hub nasce com um propósito: criar tecnologia de forma sustentável. Inspirado no encontro das águas dos rios Negro e Solimões em Manaus, este projeto representa a convergência harmoniosa entre inovação tecnológica e consciência ambiental.

Nossa missão é desenvolver soluções que não apenas automatizam e otimizam processos, mas o fazem com responsabilidade ambiental e social, criando um ecossistema digital sustentável.

## Arquitetura do Hub (Em Evolução)

Inicialmente construído em uma arquitetura "Tudo-em-Um" (Streamlit Híbrido), o Hub está **atualmente em processo de refatoração** para um ecossistema mais robusto e escalável.

A nova arquitetura desacoplada inclui:
* **`FastAPI`**: Para servir os Agentes de IA e a lógica de negócios como um backend dedicado.
* **`n8n` (Self-Hosted)**: Para orquestrar automações complexas e fluxos de trabalho.
* **`Streamlit`**: Mantido como a interface principal para o Painel de Controle e visualização de dados.

## Tecnologias Utilizadas

<div align="center">

| Categoria | Tecnologia | Descrição |
|-----------|------------|-----------|
| **Linguagem Core** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Linguagem principal |
| **Backend API** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | API para os Agentes |
| **Automação** | ![n8n](https://img.shields.io/badge/n8n-1A1A1A?style=for-the-badge&logo=n8n&logoColor=white) | Orquestração de workflows |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) | Interface do Painel |
| **IA (Multi-API)** | ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ![Gemini](https://img.shields.io/badge/Gemini-8E8E8E?style=for-the-badge&logo=google&logoColor=white) ![Claude](https://img.shields.io/badge/Claude-D97A3A?style=for-the-badge&logo=anthropic&logoColor=white) | GPT-4o-Mini, Gemini & Claude |
| **Database** | ![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white) | Armazenamento e Vetorização |
| **RAG** | ![LangChain](https://img.shields.io/badge/LangChain-020202?style=for-the-badge&logo=langchain&logoColor=white) ![ChromaDB](https://img.shields.io/badge/Chroma-555555?style=for-the-badge&logo=chroma&logoColor=white) | Orquestração e VectorDB |
| **Deploy** | ![Streamlit Cloud](https://img.shields.io/badge/Streamlit_Cloud-0D0D0D?style=for-the-badge&logo=streamlit&logoColor=white) | Hospedagem (Atual) |

</div>

## Estrutura do Repositório

```bash
encontro-dagua-hub/
├── 📂 interface/             # App híbrido (Showcase + Painel)
│   └── 📄 app.py
├── 📂 specs/                 # DNAs dos agentes especialistas
├── 📂 base_conhecimento/     # Bases RAG e documentação
├── 📄 requirements.txt       # Dependências
├── 📄 gemini.md             # Documentação do processo
├── 📄 README.md
└── 📄 LICENSE
```

## Como Começar

O projeto está **ATIVO** e em execução no Streamlit Cloud. Para desenvolvimento local:

```bash
# Clone o repositório (branch main)
git clone https://github.com/lidimoura/encontro-dagua-hub.git

# Acesse o diretório
cd encontro-dagua-hub

# Configure o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## Contribuição

Estamos em fase inicial de desenvolvimento. Em breve, disponibilizaremos guias detalhados para contribuição. Se você se identifica com nossa missão de tecnologia sustentável, fique atento às atualizações.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Contato

<div align="center">

**Lídi Moura**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lidimoura/)

</div>

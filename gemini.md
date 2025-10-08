# Gemini Deployment Log for Encontro D'Água Hub (Status: Lançado Oficialmente)

Este arquivo registra a jornada completa de arquitetura e debugging do projeto "Encontro D'Água Hub", culminando no lançamento bem-sucedido da arquitetura "Tudo-em-Um".

---

## 1. Fase 1: Arquitetura Inicial e Pivôs (06/10/2025 - 09/10/2025)

Esta seção documenta a arquitetura inicial e os desafios que levaram à decisão estratégica de pivotar.

| Data | Evento | Detalhes e Lições Aprendidas |
| :--- | :--- | :--- |
| **06/10** | **Design Inicial** | Microsserviços: API FastAPI (Cloud Run) + Interface Streamlit (Cloud). Motor: Google Gemini API (bloqueado). |
| **07/10** | **Refatoração de IA** | Migração do RAG para Vertex AI (`discoveryengine`) e criação do **Agente Gerente** (`agente_gerente_v1`). |
| **09/10** | **Pivô para OpenAI** | Substituição da stack Google por `openai` e `langchain-openai`. Tentativa de resolver *cold start* com padrão Singleton no Cloud Run. |
| **Falha Crítica** | **Cloud Run Timeout** | O *deployment* falhou consistentemente devido a *timeouts* e à complexidade de gerenciar a API e a Interface separadamente. |

---

## 2. Fase 2: Arquitetura "Tudo-em-Um" (Lançamento Oficial)

A partir de 08/10/2025, foi adotada a arquitetura antifrágil, focada em funcionalidade imediata e agilidade, resultando no lançamento bem-sucedido do Hub.

### 2.1. Configuração de Deployment e Stack

O **Pivô Estratégico Final** consolidou todos os componentes em uma única aplicação Streamlit.

| Componente | Tecnologia | Configuração Final |
| :--- | :--- | :--- |
| **Design** | **"Tudo-em-Um"** (Monolítico Simples) | Toda a lógica reside em um único arquivo (`interface/app.py`). |
| **Deployment Oficial** | **Streamlit Community Cloud** | *Deployment* realizado via GitHub (branch `develop`), utilizando o `requirements.txt` na raiz. |
| **Motor (LLM)** | **OpenAI (`gpt-3.5-turbo`)** | Cérebro de todos os Agentes. |
| **RAG (Conhecimento)** | **LangChain + ChromaDB** | Utiliza `@st.cache_resource` para carregamento instantâneo do Vector Store. |
| **Processamento RAG** | **`UnstructuredFileLoader`** | Implementado para garantir a leitura correta e formatada de arquivos `.md` (resolvendo o erro `'str' object has no attribute 'page_content'`). |
| **Memória Persistente** | **Supabase (`supabase`)** | Armazena o histórico do chat (`chat_memory`). O erro de instalação `supabase-py` foi corrigido para o pacote correto `supabase`. |

### 2.3. Lógica de Agentes (Orquestração)

* **Nomenclatura:** "Gems" renomeados para **Agentes**.
* **Orquestrador:** O **`agente_gerente_v3`** é a porta de entrada.
* **Regras de Orquestração:** O DNA (`v3`) foi rigidamente configurado para:
    * **REGRA 1 (Gerenciamento de Projetos):** Define a sequência correta de execução dos 9 especialistas (ex: Briefing $\rightarrow$ Arquiteto Web $\rightarrow$ Lovable Prompter $\rightarrow$ QA).
    * **REGRA 3 (Roteamento):** Envia o comando exato `DELEGAR: [ID do Agente]` (Antihallucination).

## 3. Resumo da Organização Final do Repositório

O repositório foi limpo para refletir a arquitetura "Tudo-em-Um".

* A pasta **`api_backend/`** foi removida.
* Os ativos de conhecimento e especificação foram centralizados nas pastas **`base_conhecimento/`** e **`specs/`** na raiz.

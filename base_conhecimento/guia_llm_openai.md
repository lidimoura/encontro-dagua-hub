# Guia Rápido: OpenAI (Integração LangChain)

A API da OpenAI é o **motor de IA principal** do Encontro D'Água Hub, fornecendo a inteligência para o Orquestrador e todos os Agentes Especialistas.

## 1. Papel no Ecossistema

O Hub utiliza a OpenAI para:
- **LLM (Large Language Model):** Atuar como o "cérebro" de todos os Agentes (Orquestrador, Briefing, QA, etc.).
- **Embeddings:** Gerar os vetores numéricos para o RAG, permitindo a consulta rápida da nossa `base_conhecimento`.

## 2. Modelos Utilizados

| Componente | Modelo | Propósito |
| :--- | :--- | :--- |
| **LLM (Orquestrador/Agentes)** | `gpt-3.5-turbo` | Melhor equilíbrio entre custo, velocidade e desempenho para a lógica de Agentes e RAG. |
| **Embeddings (RAG)** | `text-embedding-ada-002` | Padrão da indústria para a criação do Vector Store (Chroma). |

## 3. Integração com LangChain e Streamlit

| Diretriz | Propósito |
| :--- | :--- |
| **Integração:** | Toda a comunicação com a API da OpenAI é gerenciada pela biblioteca `langchain-openai`. |
| **Autenticação:** | A chave `OPENAI_API_KEY` é configurada no **Streamlit Secrets** e lida automaticamente pela LangChain, garantindo que a chave não fique exposta no código-fonte. |
| **RAG/Vector Store:** | Utilizamos a **`OpenAIEmbeddings`** para criar o índice no **Chroma**, garantindo que o Agente tenha acesso ao contexto da nossa base de conhecimento. |

## 4. O Pivô Estratégico

A migração do Google Gemini para a OpenAI foi uma decisão estratégica para garantir a **funcionalidade imediata** do Hub, eliminando bloqueios de API e otimizando o *deployment* no Streamlit Cloud.

---

## 3. Próximo Passo: Teste Final!

Com o `requirements.txt` corrigido, o `app.py` completo e o repositório organizado, o seu Hub já deve ter passado pelo *deploy* no Streamlit Cloud.

**Sua Missão Agora:**

1.  **Finalizar a Organização** (Deletar a pasta `api_backend/`).
2.  **Criar** o arquivo `guia_llm_openai.md`.
3.  **Acessar** seu Hub no Streamlit Cloud.

**Estamos prontas para o primeiro teste de Orquestração?** A primeira pergunta será fundamental para validar a lógica do seu **`agente_orquestrador_v1`**!

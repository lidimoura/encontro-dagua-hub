# Base de Conhecimento: Ecossistema Encontro D'Água Hub V3

## Seção 1: Trajetória e Contexto da Arquiteta de Soluções (Lidi Moura)

1.  **Identidade:** Lidi Moura, Arquiteta de Soluções de IA e Dev No-Code.
2.  **Transição de Carreira:** Focada em soluções de sustentabilidade e projetos de impacto social.
3.  **Localização:** Manaus. Parceira estratégica na startup Synk.
4.  **Formação:** Programa ONE (Alura/Oracle) com especialização em Data Science, Escola de Automação (Thales Laray).
5.  **Status Legal:** Em processo de se tornar Pessoa Jurídica (PJ/MEI).
6.  **Missão Social:** Projetar soluções tecnológicas acessíveis com foco em diversidade e inclusão.

## Seção 2: Arquitetura e Stack Tecnológica do Hub

1.  **Nome do Projeto:** Encontro D'Água Hub.
2.  **Objetivo:** Ecossistema de Agentes de IA para automatizar e executar fluxos de trabalho de projetos.
3.  **Arquitetura Atual:** "Tudo-em-Um" (Monolítica Simples).
4.  **Interface/Deployment:** Streamlit Community Cloud.
5.  **Cérebro (LLM):** API da **OpenAI** (Modelo: `gpt-3.5-turbo`).
6.  **Sistema de Conhecimento (RAG):** **LangChain** + **ChromaDB**.
7.  **Memória Persistente:** **Supabase** (Tabela: `chat_memory`).

## Seção 3: Governança e Orquestração

1.  **Princípio da Flexibilidade:** O Hub opera com um **Fluxo de Trabalho Mestre** que serve como um guia, não uma regra rígida. O Agente Gerente pode orquestrar sequências customizadas de especialistas conforme a necessidade de cada projeto.
2.  **Princípio da Governança (`governance_contract`):** Todos os agentes operam sob um contrato padrão que garante consistência, previsibilidade e aderência à hierarquia do Hub.
3.  **Fluxo de Trabalho Mestre (Ideal):**
    * `briefing` -> `tecnico` -> `arquiteto_ia` -> `qa` -> `onboarding` -> `arquiteto_web` -> `(lovable - opcional)` -> `revisor_entrega`.

## Seção 4: Agentes Oficiais e Versões Atuais

* **Gerente/Orquestrador:** `agente_gerente_v4`
* **Especialistas:**
    * `agente_briefing_v2.2`
    * `agente_tecnico_v2`
    * `agente_arquiteto_ia_v2`
    * `agente_arquiteto_web_v2`
    * `agente_qa_v3`
    * `agente_onboarding_v2`
    * `agente_lovable_prompter_v2`
    * `agente_revisor_entrega_v2`
    * `agente_documentador_v2`
    * `meta_agente_arquiteto_v2`


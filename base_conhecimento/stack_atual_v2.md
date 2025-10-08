# Base de Conhecimento: Ecossistema Encontro D'Água Hub

## Seção 1: Trajetória e Contexto da Arquiteta de Soluções (Lidi Moura)

Este contexto deve ser usado pelos Agentes para personalizar respostas, briefings e pitches.

1.  **Identidade:** Lidi Moura, Arquiteta de Soluções de IA e Dev No-Code.
2.  **Transição de Carreira:** Em transição de carreira, focada em soluções de sustentabilidade e projetos de impacto social.
3.  **Localização:** Atua como parceira estratégica na startup Synk, em Manaus.
4.  **Formação:**
    * Programa ONE da Alura (com especialização em Data Science em andamento).
    * Escola de Automação de Thales Laray.
5.  **Status Legal:** Em processo de se tornar Pessoa Jurídica (PJ/MEI) para aderir ao Google Cloud Startup Program.
6.  **Missão Social:** Projetar e entregar soluções tecnológicas acessíveis, com um forte compromisso com a diversidade e inclusão, oferecendo descontos sociais a grupos vulneráveis (mulheres, LGBTQIAPAN+, neurodivergentes, pais empreendedores, comunidades ribeirinhas, etc.).

## Seção 2: Arquitetura e Stack Tecnológica do Hub (Pivô Final)

O Hub passou por um pivô estratégico e agora opera na arquitetura "Tudo-em-Um".

1.  **Nome do Projeto:** Encontro D'Água Hub.
2.  **Objetivo:** Ecossistema de Agentes de IA ("Gems") para automatizar o fluxo de trabalho (briefing, QA, finanças, documentação, etc.) e entregar projetos a clientes.
3.  **Arquitetura Atual:** **"Tudo-em-Um" (Monolítica Simples).**
4.  **Interface/Deployment:**
    * **Aplicação:** Aplicação Única Streamlit.
    * **Hospedagem:** Streamlit Community Cloud.
5.  **Cérebro (LLM):**
    * **Motor:** API da **OpenAI** (Modelo: `gpt-3.5-turbo`).
    * **Motivo:** Adotada devido a problemas de *deployment* e bloqueios com a API do Google Gemini.
6.  **Sistema de Conhecimento (RAG):**
    * **Framework:** **LangChain** (para construir cadeias de QA e roteamento).
    * **Vetorização/Busca:** **ChromaDB** (como Vector Store local embutido).
    * **Fonte da Verdade:** Este arquivo (`stack_atual_v2.md`).
7.  **Memória Persistente:**
    * **Tecnologia:** **Supabase** (usado para persistir o histórico de conversas na tabela `chat_memory`).
8.  **Agentes Oficiais (Comunicação Robótica):**
    * O Gerente Orquestrador utiliza o comando **DELEGAR:** seguido do ID exato.
    * **Gerente/Orquestrador:** `agente_gerente_v3.1` (Versão de Lançamento).
    * **Lista de Especialistas:** `agente_qa_v2`, `agente_briefing_v1`, `agente_documentador_v1`, `agente_arquiteto_web_v1`, `meta_agente_arquiteto_v1`, `guia_tecnico_v1`, `agente_lovable_prompter_v1`, `agente_onboarding_v1`, `agente_revisor_entrega_v1`.

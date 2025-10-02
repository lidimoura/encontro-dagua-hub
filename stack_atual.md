%%writefile "/content/drive/MyDrive/encontro-dagua-hub/knowledge_base/stack_atual.md"
# 📚 Stack Tecnológico e Diretrizes - Encontro D'Água Hub

**Versão:** 1.0
**Última Atualização:** 30 de setembro de 2025

Este documento é a fonte oficial de verdade sobre as tecnologias utilizadas no ecossistema do Encontro D'Água Hub. Ele serve como base de conhecimento para todos os Gems e processos de desenvolvimento, garantindo que as ferramentas sejam utilizadas de forma consciente, sustentável e padronizada.

---

## 🏛️ Core do Hub (Desenvolvimento Principal)

Estas são as tecnologias centrais que formam a espinha dorsal do nosso software.

### Python
-   **Papel no Ecossistema:** A linguagem de programação fundamental para toda a nossa lógica de backend, automações e a inteligência dos Gems.
-   **Diretrizes de Uso:**
    -   Utilizar sempre a versão 3.10 ou superior.
    -   Todos os projetos devem usar ambientes virtuais (`.venv`).
    -   O código deve ser formatado utilizando o `black` para manter a consistência.

### FastAPI
-   **Papel no Ecossistema:** O framework Python que usamos para construir nosso "motor" (a API de backend). Ele é responsável por receber requisições, processar a lógica e se comunicar com os outros serviços.
-   **Diretrizes de Uso:**
    -   Sempre utilizar `Pydantic` para validação de dados nas requisições e respostas.
    -   Priorizar rotas assíncronas (`async def`) para melhor performance.

### Google Gemini
-   **Papel no Ecossistema:** O cérebro generativo e a inteligência artificial por trás de todos os Gems. É a API que consultamos para obter respostas, análises e conteúdo.
-   **Diretrizes de Uso:**
    -   Os prompts enviados ao Gemini devem seguir rigorosamente o blueprint gerado pelo "Meta-Gem Arquiteto".
    -   Deve-se sempre avaliar o custo-benefício do modelo a ser utilizado (ex: usar um modelo mais simples e rápido para tarefas simples).

### Supabase
-   **Papel no Ecossistema:** Nossa memória persistente. É o banco de dados Postgres onde armazenamos o "Diário de Logs" das interações dos Gems, permitindo aprendizado e consistência a longo prazo.
-   **Diretrizes de Uso:**
    -   A tabela principal é a `gem_logs`.
    -   A interação com o Supabase deve ser feita através do cliente Python oficial.

### Streamlit & Lovable
-   **Papel no Ecossistema:** Nossas ferramentas de prototipagem de interface (frontend).
-   **Diretrizes de Uso:**
    -   **Streamlit:** Utilizado para criar painéis de controle internos e ferramentas de teste rápidas.
    -   **Lovable:** Utilizado para prototipar interfaces mais complexas e visualmente elaboradas para apresentação a clientes.

### LangChain
-   **Papel no Ecossistema:** A "biblioteca" do nosso sistema. É o framework que conecta o Gemini à nossa base de conhecimento (`/knowledge_base`), permitindo o processo de RAG (Retrieval-Augmented Generation).
-   **Diretrizes de Uso:**
    -   Utilizar para carregar documentos, dividir textos (chunking) e criar as cadeias de busca de informação.

---

## 🏗️ Infraestrutura e Deploy

Ferramentas que suportam nosso desenvolvimento e colocam nosso projeto no ar.

### Git & GitHub
-   **Papel no Ecossistema:** Nosso sistema de controle de versão e o hub central do nosso código (o monorepo `encontro-dagua-hub`).
-   **Diretrizes de Uso:**
    -   Todo o trabalho deve ser feito em branches separadas, nunca diretamente na `main`.
    -   As mensagens de commit devem seguir um padrão (ex: `feat: adiciona endpoint de QA`).

### Render & Streamlit Community Cloud
-   **Papel no Ecossistema:** Nossas plataformas de hospedagem **gratuitas** para a fase de desenvolvimento e prototipagem.
-   **Diretrizes de Uso:**
    -   **Render:** Usado para o deploy da API em FastAPI. Lembrar da limitação do "sleep" no plano gratuito.
    -   **Streamlit Cloud:** Usado para o deploy das interfaces em Streamlit.

### Hostinger
-   **Papel no Ecossistema:** Nossa plataforma de hospedagem **de produção** (plano futuro). É para onde o projeto migrará quando estiver maduro e pronto para o público geral ou clientes.

---

## 🛠️ Stack Estendido (Low-Code/No-Code)

Estas são ferramentas adicionais do seu stack de trabalho. Os Gems devem estar cientes delas para dar suporte a projetos de clientes que as utilizem.

### gptmaker, typebot, manychat
-   **Papel no Ecossistema:** Plataformas para criação de chatbots e fluxos conversacionais.
-   **Contexto:** Utilizadas principalmente em projetos de automação de atendimento para clientes.

### Make (anteriormente Integromat)
-   **Papel no Ecossistema:** A "cola" de automação visual. É a principal ferramenta para integrar diferentes APIs e serviços sem a necessidade de código complexo.
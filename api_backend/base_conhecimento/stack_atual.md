# 📚 Stack Tecnológico e Diretrizes - Encontro D'Água Hub v2.0

**Última Atualização:** 04 de outubro de 2025

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
    -   Os prompts enviados ao Gemini devem seguir rigorosamente o blueprint ("DNA") do Gem especialista definido na pasta `/specs`.
    -   O "Gem Gerente" pode escolher o modelo mais apropriado para a tarefa (ex: `flash` para rapidez, `pro` para complexidade) visando eficiência de custo.

### Supabase
-   **Papel no Ecossistema:** Nossa memória persistente. É o banco de dados Postgres onde armazenamos o "Diário de Logs" (`gem_logs`) das interações dos Gems, permitindo aprendizado e consistência a longo prazo.
-   **Diretrizes de Uso:**
    -   A interação deve ser feita via a biblioteca cliente do Python.
    -   A RLS (Row-Level Security) deve ser mantida desativada para a API ter acesso total.

### Streamlit & Lovable
-   **Papel no Ecossistema:** Nossas ferramentas de prototipagem e construção de interface (frontend).
-   **Diretrizes de Uso:**
    -   **Streamlit:** Utilizado para criar painéis de controle internos e protótipos funcionais rápidos.
    -   **Lovable:** Utilizado para prototipar interfaces mais complexas e visualmente elaboradas para apresentação e validação com clientes.

### LangChain
-   **Papel no Ecossistema:** A "biblioteca" do nosso sistema. É o framework que conecta o Gemini à nossa base de conhecimento (`/base_conhecimento`), permitindo o processo de RAG (Retrieval-Augmented Generation).
-   **Diretrizes de Uso:**
    -   Utilizar para carregar documentos, dividir textos (chunking) e criar as cadeias de busca de informação.

---

## 🏗️ Infraestrutura e Deploy

Ferramentas que suportam nosso desenvolvimento e colocam nosso projeto no ar.

### Git & GitHub
-   **Papel no Ecossistema:** Nosso sistema de controle de versão e o hub central do nosso código (o monorepo `encontro-dagua-hub`).
-   **Diretrizes de Uso:**
    -   Todo o desenvolvimento de novas funcionalidades acontece em branches separadas (como a `develop`).
    -   A branch `main` é a versão estável ("Rio Negro"). As mudanças só são integradas via Pull Request.

### Docker
-   **Papel no Ecossistema:** A nossa "fábrica de caixas". É a ferramenta que usamos para empacotar nossa API FastAPI em um contêiner padronizado, garantindo que ela rode da mesma forma em qualquer lugar.

### Google Cloud Run
-   **Papel no Ecossistema:** A casa da nossa API. É a plataforma serverless onde nossa aplicação em contêiner (a "caixa" do Docker) é hospedada e executada.

### Streamlit Community Cloud
-   **Papel no Ecossistema:** A casa da nossa interface. É a plataforma gratuita onde hospedamos nossa aplicação Streamlit.

---

## 🛠️ Stack Estendido (Low-Code/No-Code)

Estas são ferramentas adicionais do seu stack de trabalho. Os Gems devem estar cientes delas para dar suporte a projetos de clientes que as utilizem.

### gptmaker, typebot, manychat
-   **Papel no Ecossistema:** Plataformas para criação de chatbots e fluxos conversacionais.
-   **Contexto:** Utilizadas principalmente em projetos de automação de atendimento para clientes.

### Make (anteriormente Integromat)
-   **Papel no Ecossistema:** A "cola" de automação visual. É a principal ferramenta para integrar diferentes APIs e serviços sem a necessidade de código complexo.

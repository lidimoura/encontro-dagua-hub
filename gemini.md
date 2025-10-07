# Gemini Deployment Log for Encontro d'Água Hub

Este arquivo registra o progresso do deployment do projeto "Encontro d'Água Hub" com a ajuda do Gemini.

## Análise do Projeto (06/10/2025)

O projeto está estruturado como um monorepo com dois serviços principais:

1.  **Backend API (`api_backend/`)**:
    *   **Framework**: FastAPI
    *   **Objetivo**: Servir como o "cérebro" do sistema, orquestrando os agentes de IA (Gems).
    *   **Deployment**: Possui um `Dockerfile` na raiz do projeto (`/encontro-dagua-hub/Dockerfile`) para containerização. Este Dockerfile está configurado para expor a porta 8080 e iniciar o servidor com `uvicorn`.

2.  **Interface (`interface/`)**:
    *   **Framework**: Streamlit
    *   **Objetivo**: Prover um painel de controle para interagir com os Gems.
    *   **Deployment**: Possui seu próprio `Dockerfile` (`/encontro-dagua-hub/interface/Dockerfile`) para containerização. Este está configurado para expor a porta 8080 e iniciar a aplicação com `streamlit run`.

## Backend API Deployment (06/10/2025)

1.  **Build Docker Image**:
    *   Comando: `docker build -t encontro-dagua-hub-api -f /home/lidimfc/encontro-dagua-hub/Dockerfile /home/lidimfc/encontro-dagua-hub`
    *   Status: Concluído com sucesso.

2.  **Push to Artifact Registry**:
    *   A imagem foi tagueada como `southamerica-east1-docker.pkg.dev/gen-lang-client-0133480655/encontro-dagua-hub-repo/encontro-dagua-hub-api:latest`.
    *   O repositório `encontro-dagua-hub-repo` foi criado no Artifact Registry.
    *   Comando: `docker push southamerica-east1-docker.pkg.dev/gen-lang-client-0133480655/encontro-dagua-hub-repo/encontro-dagua-hub-api:latest`
    *   Status: Concluído com sucesso.

3.  **Deploy to Cloud Run**:
    *   Próximo passo.

## Refatoração da Arquitetura de IA (07/10/2025)

Com o objetivo de profissionalizar e otimizar o Hub, uma refatoração significativa foi realizada na arquitetura de IA, com as seguintes mudanças:

1.  **Migração para o RAG Engine do Vertex AI**:
    *   **O que mudou**: A biblioteca `llama_index`, que recriava o índice de conhecimento a cada chamada, foi completamente removida do backend (`api_backend/main.py`).
    *   **Nova Abordagem**: O backend agora se comunica diretamente com o **RAG Engine** provisionado no Vertex AI (`ragCorpora/6917529027641081856`). A função `retrieve_rag_contexts` utiliza a API `discoveryengine` para uma busca de contexto muito mais rápida e escalável.
    *   **Benefício**: Performance drasticamente melhorada e separação de responsabilidades, alinhando o projeto com as melhores práticas de nuvem.

2.  **Criação do "Gem Gerente" (Orquestrador)**:
    *   **O que mudou**: Foi introduzido um novo agente, o `gem_gerente_v1`, cujo DNA (`specs/gem_gerente_v1.md`) o instrui a atuar como um roteador inteligente.
    *   **Nova Abordagem**: Ao receber uma pergunta, o "Gem Gerente" analisa a intenção e escolhe o Gem especialista mais adequado da sua lista de conhecimento. A função `select_specialist_gem` no backend implementa essa lógica.
    *   **Benefício**: Simplifica a experiência do usuário, que não precisa mais saber qual especialista escolher. O Hub se torna mais autônomo.
 
## Evolução do Gem Gerente para Orquestrador (08/10/2025)

Com o objetivo de aumentar a autonomia e a inteligência do Hub, o Gem Gerente evoluiu de um simples roteador para um verdadeiro orquestrador de soluções.

1.  **Inteligência Aprimorada no Blueprint**:
    *   **O que mudou**: O DNA do `gem_gerente_v1` (`specs/gem_gerente_v1.md`) foi completamente reescrito.
    *   **Nova Abordagem**: O gerente agora possui 3 comportamentos principais, definidos por regras claras:
        1.  **Resposta Direta**: Se a pergunta é sobre o Hub ou seus processos, ele mesmo responde usando o RAG.
        2.  **Plano de Ação**: Se o usuário quer iniciar um novo projeto, ele descreve o plano sequencial de Gems a serem usados.
        3.  **Roteamento Pontual**: Se a tarefa é específica para um especialista, ele delega retornando o ID do Gem.
    *   **Benefício**: O Hub se torna capaz de lidar com ambiguidades e tarefas complexas de ponta a ponta.

2.  **Adaptação do Backend (`main.py`)**:
    *   **O que mudou**: A função `invoke_gem` foi atualizada para interpretar a nova capacidade do gerente.
    *   **Nova Abordagem**: A API agora verifica a resposta do `gem_gerente_v1`. Se a resposta não for um ID de Gem válido, ela é tratada como uma resposta final (um plano ou informação) e retornada diretamente ao usuário, encerrando o fluxo. Se for um ID, o fluxo de RAG e geração de resposta continua normalmente com o Gem especialista escolhido.
    *   **Benefício**: A API se torna flexível, suportando tanto a delegação de tarefas quanto a entrega de respostas diretas pelo orquestrador.

## Pivô Estratégico para OpenAI e LangChain (09/10/2025)

Após semanas de desafios persistentes com o deploy no Google Cloud Run, que resultaram em um looping de erros de `ModuleNotFoundError` e `Container failed to start`, foi tomada a decisão estratégica de pivotar a stack de IA para uma arquitetura mais robusta e padrão de mercado.

1.  **Migração do Backend de IA**:
    *   **O que mudou**: As bibliotecas `google-cloud-discoveryengine` e `google-cloud-aiplatform` foram removidas. Foram adicionadas as bibliotecas `openai`, `langchain`, `chromadb` e suas dependências.
    *   **Nova Abordagem**: O arquivo `api_backend/main.py` foi completamente refatorado. A lógica de RAG agora é construída com LangChain, utilizando `ChatOpenAI` como LLM, `OpenAIEmbeddings` para vetorização e `Chroma` como banco de dados vetorial em memória.
    *   **Benefício**: Maior estabilidade, portabilidade e uma base de código mais fácil de depurar, alinhada com tutoriais e comunidades de IA. A lógica do "Gem Gerente" foi preservada e adaptada para a nova stack.

2.  **Gerenciamento de Segredos**:
    *   **O que mudou**: A chave `GOOGLE_API_KEY` foi substituída pela `OPENAI_API_KEY`.
    *   **Nova Abordagem**: A nova chave da OpenAI foi adicionada ao Google Secret Manager e conectada ao serviço do Cloud Run, mantendo as melhores práticas de segurança.

## Otimização de Inicialização (Cold Start) no Cloud Run (09/10/2025)

Mesmo após o pivô, o deploy enfrentou um erro de `Container failed to start` devido ao tempo de inicialização.

1.  **Diagnóstico**: A criação do índice vetorial (RAG) estava ocorrendo no escopo global do `main.py`, sendo executada durante a inicialização do contêiner. Em ambientes serverless, isso pode exceder o tempo limite de startup.
2.  **Solução**:
    *   **O que mudou**: O `main.py` foi refatorado para usar um padrão "Singleton" (lazy loading) para o carregamento do RAG.
    *   **Nova Abordagem**: A função `carregar_e_processar_documentos` agora só é chamada dentro do endpoint `invoke_gem`. Ela armazena o índice em uma variável global e só executa o trabalho pesado de carregar e processar os documentos na **primeira chamada** à API, sendo instantânea nas chamadas subsequentes.
    *   **Benefício**: Reduz drasticamente o tempo de inicialização do contêiner, resolvendo o erro de timeout e melhorando a performance em "cold starts".
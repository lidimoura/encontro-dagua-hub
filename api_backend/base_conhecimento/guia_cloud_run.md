# Guia Rápido: Google Cloud Run

O Google Cloud Run é a **"casa" oficial da nossa API FastAPI**.

### 1. O que é o Cloud Run?
É uma plataforma *serverless* que executa nossos contêineres Docker. Isso significa que não precisamos gerenciar servidores; o Google cuida da infraestrutura.

### 2. Tipos de Execução
| Tipo de Recurso | Descrição | Uso no Hub |
| :--- | :--- | :--- |
| **Service (Serviço)** | Responde a requisições HTTP, escalando automaticamente de zero a milhares de instâncias. | É o que usamos para hospedar nossa API "Gem Gerente". |
| **Job (Tarefa)** | Executa tarefas que têm um início e um fim, sem responder a requisições web. | Poderíamos usar no futuro para tarefas como "re-indexar toda a base de conhecimento". |

### 3. Lições Aprendidas no Deploy do Hub
- **`Creating Revision...failed` (Erro de Timeout):** Este erro geralmente indica que a aplicação no contêiner falhou ao iniciar, muitas vezes por falta de uma variável de ambiente (como a `GOOGLE_API_KEY`) ou um erro de código no startup. A solução é **investigar os logs do Cloud Run**.
- **`Build failed` (Erro de Construção):** Este erro indica um problema no `Dockerfile` ou nos arquivos que ele tenta copiar. A solução é **investigar os logs do Cloud Build** para encontrar a linha exata que falhou (ex: `COPY failed`).
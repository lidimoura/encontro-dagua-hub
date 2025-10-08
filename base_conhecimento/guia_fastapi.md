#### **`guia_fastapi.md`**
```markdown
# Guia Rápido: FastAPI

O FastAPI é o **"motor"** do nosso backend, a fundação da nossa API "Gem Gerente".

### 1. O que é FastAPI?
É o framework Python que utilizamos para construir nossa API. Ele é responsável por:
- Receber requisições HTTP.
- Processar a lógica de negócio.
- Comunicar-se com outros serviços (como a API Gemini).

### 2. Diretrizes de Uso no Hub
| Diretriz | Propósito |
| :--- | :--- |
| **Validação com Pydantic** | Sempre usar `Pydantic` para validar os dados que entram e saem da API, garantindo robustez. |
| **Performance com `async`** | Priorizar rotas assíncronas (`async def`) para obter o melhor desempenho. |
| **Estrutura Profissional** | O código deve ser organizado em uma estrutura de aplicação (ex: `main.py`, `requirements.txt`) para o deploy. |

### 3. Execução e Documentação
- **Execução:** O servidor é iniciado com o `uvicorn`.
- **Documentação Automática:** O FastAPI gera automaticamente uma documentação interativa da nossa API, acessível em `/docs` no ambiente de desenvolvimento.

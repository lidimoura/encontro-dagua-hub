# Guia Rápido: Google Gemini API

A Gemini API é a interface que permite ao nosso Hub interagir com os modelos de IA da Google. É o "cérebro" dos nossos Gems.

### 1. Endpoints Principais
A API é organizada em torno de endpoints que definem como interagimos com o modelo:

| Endpoint | Descrição | Uso Ideal no Hub |
| :--- | :--- | :--- |
| **`generateContent`** | Processa a requisição e retorna a resposta completa de uma vez. | Perfeito para a nossa API, onde aguardamos o resultado total. |
| **`streamGenerateContent`** | Envia a resposta em "pedaços" (chunks) conforme são gerados. | Ideal para futuras interfaces de chat mais interativas, que mostram o texto sendo "digitado". |

### 2. Autenticação
Toda requisição para a API deve incluir nossa chave de API no cabeçalho (`header`):
- **Cabeçalho:** `x-goog-api-key`
- **Origem:** A chave é gerada no Google AI Studio e configurada como um segredo nos nossos ambientes (Cloud Run, Streamlit Cloud).

### 3. Exemplo Prático de Requisição (`curl`)
Este é um exemplo de uma chamada direta à API para gerar conteúdo a partir de um prompt de texto.

```bash
curl "[https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent](https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent)" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explique como a IA funciona em um único parágrafo."
          }
        ]
      }
    ]
  }'
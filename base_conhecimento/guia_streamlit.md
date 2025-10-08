# Guia Rápido: Streamlit

O Streamlit é nossa ferramenta de **prototipagem rápida e painéis internos**.

### 1. Papel no Ecossistema
- **Painéis Internos:** Usado para criar o "Painel de Comando do Hub".
- **Protótipos Rápidos:** Essencial para criar e validar interfaces funcionais com velocidade.

### 2. Estratégia de Deploy
- **Plataforma Padrão:** A hospedagem é feita na **Streamlit Community Cloud**.
- **Ambiente Descartado:** O teste no Cloud Shell Editor foi abandonado devido a problemas persistentes de conexão (`timeout`).

### 3. Dica Prática de Dependências
- A organização das dependências é crucial. O deploy depende de um arquivo `requirements.txt` na **raiz** do projeto. A ausência de uma biblioteca (como `supabase`) neste arquivo causou `ModuleNotFoundError`.

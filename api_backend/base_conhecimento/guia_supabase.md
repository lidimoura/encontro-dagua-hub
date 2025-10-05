# Guia Rápido: Supabase

O Supabase desempenha o papel de **memória persistente** em nosso ecossistema.

### 1. Conceito Central
- **O que é:** Nosso banco de dados Postgres.
- **Uso Principal:** Armazenar a tabela `gem_logs` com as interações dos Gems, permitindo consistência e aprendizado contextual.

### 2. Componentes de Interação
- **Linguagem:** Interagimos com o Supabase via Python.
- **Biblioteca:** A interação deve ser feita pela biblioteca cliente `supabase-py`.

### 3. Diretrizes Críticas (Lições Aprendidas)
- **RLS (Row-Level Security):** Deve ser mantida **desativada** na tabela `gem_logs` para garantir que a API do Hub tenha acesso total. A ativação incorreta causou erros de permissão.
- **Dependências:** A biblioteca `supabase` deve estar explicitamente no `requirements.txt` da raiz do projeto para evitar `ModuleNotFoundError` no deploy do Streamlit.
- **Lógica de Código:** A sintaxe de `insert` e `update` deve ser validada para evitar erros de atributo. A lógica de "inserir-e-depois-atualizar-pelo-ID" provou ser a mais robusta.
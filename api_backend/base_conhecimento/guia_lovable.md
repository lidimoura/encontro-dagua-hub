# Guia Rápido: Lovable.ai

Este guia compila os principais insights e boas práticas para usar o Lovable no ecossistema do Encontro D'Água Hub, garantindo a estabilidade do código gerado (React/Vite/Tailwind) e a integração com nosso backend (Python/FastAPI).

### 1. Estratégias de Prompt e Qualidade

| Insight | Descrição e Ação Prática |
| :--- | :--- |
| **Prompt Inicial de Alta Qualidade** | Invista tempo para refinar sua descrição inicial. Um erro de um grau no início pode resultar em um desalinhamento enorme após 100 prompts. |
| **Refatoração Constante** | O código gerado tende a ficar "bugado" e inchado após ~300 mensagens. Use prompts de refatoração regularmente para modularizar o código e manter o projeto estável. |
| **Uso de "Knowledge"** | Use a funcionalidade "Knowledge" nas configurações do Lovable para adicionar padrões de codificação, guias de estilo ou documentação. Isso garante consistência. |
| **Precisão com Seleção de UI** | Para evitar que o Lovable altere o elemento errado, clique e selecione o item específico na interface antes de enviar seu prompt de alteração. |
| **Edição Direta de Código** | Para alterações pequenas (textos, CSS), edite o código diretamente na interface do Lovable para economizar créditos e tempo. |

### 2. Considerações de Stack e Integração

| Insight | Relevância para o Stack do Hub |
| :--- | :--- |
| **Estabilidade e Stack Fechado** | O Lovable adota uma stack "apertada" (React, Vite, Tailwind), o que reduz erros e bugs no código de frontend (JS/HTML/CSS) gerado. |
| **Integração com Supabase** | A integração do Lovable com o Supabase é descrita como "super suave" e rápida, excelente para conectar à nossa memória persistente (`gem_logs`). |
| **O Dilema do GitHub** | A integração com o GitHub gera um commit para cada diálogo, resultando em um histórico caótico. **Decisão:** Desenvolver no Lovable e só então mover o código de forma controlada para o nosso repositório. |

### 3. Limitações de Arquitetura

| Insight | Limitação e Recomendação de Uso |
| :--- | :--- |
| **Bias para SPA (Single Page App)** | O Lovable tende a construir aplicações de página única, onde a URL não muda. Isso pode ser ruim para SEO e indexação. |
| **Função Ideal no Hub** | O Lovable é melhor utilizado para **protótipos funcionais rápidos** ou **landing pages únicas**, onde SEO profundo não é a prioridade inicial. |
| **O Limite da Estabilidade** | Após ~300 mensagens, o tempo gasto debugando pode superar o tempo de desenvolvimento. Este é o ponto para considerar a migração para um ambiente de código mais controlado. |
### Guia Rápido Lovable: Insights e Boas Práticas (Compatibilidade com o Stack do Hub)

#### 1. Estratégias de Prompt e Qualidade do Código

O segredo para um código limpo e estável reside em como você se comunica com a IA.

| Insight | Descrição e Ação Prática |
| :--- | :--- |
| **Prompt Inicial de Alta Qualidade** | O prompt de partida define a trajetória. Um erro de 1 grau no início resulta em grande desalinhamento. Invista tempo para refinar sua descrição inicial. |
| **Refatoração Constante** | O código gerado tende a ficar "bugado" e inchado (bloated) após ~300 mensagens. Use prompts de refatoração regularmente para modularizar o código. |
| **Uso de "Knowledge"** | Na seção de configurações do Lovable, adicione padrões de codificação e guias de estilo (cores, etc.) para garantir consistência técnica e visual. |
| **Precisão com Seleção de UI** | Para evitar que o Lovable altere o elemento errado, clique e selecione o item específico na interface antes de enviar o prompt de alteração. |
| **Edição Direta de Código** | Para alterações pequenas (textos, CSS), edite o código diretamente na interface do Lovable. Economiza créditos e tempo. |
| **Automação de Prompts** | Instale uma extensão de "text expander" para salvar e inserir rapidamente prompts complexos e repetitivos (ex: auditoria de refatoração). |

#### 2. Considerações Técnicas e de Stack

O Lovable utiliza uma stack fechada (React, Vite, Tailwind), compatível com os requisitos de frontend do Hub.

| Insight | Relevância para o Stack do Hub |
| :--- | :--- |
| **Estabilidade e Stack Fechado** | O Lovable é considerado estável por ter uma stack "apertada" e opinativa, o que reduz erros no código gerado (JavaScript/HTML/CSS). |
| **Integração com Supabase** | A integração com o Supabase é descrita como "super suave" e rápida, o que é excelente para conectar a memória persistente (`gem_logs`) do Hub. |
| **Viabilidade para Complexidade** | O Lovable é capaz de construir projetos full-stack complexos, conectando-se ao nosso backend FastAPI/Python via API. |
| **O Dilema do GitHub** | A integração com o GitHub gera um commit para cada mensagem do chat, resultando em um histórico de commits caótico. Recomenda-se desenvolver no Lovable e só depois integrar ao Git. |

#### 3. Limitações de Arquitetura

| Insight | Limitação e Recomendação de Uso |
| :--- | :--- |
| **Bias para SPA (Single Page App)** | O Lovable tende a construir aplicações de página única (SPA), onde a URL não muda ao navegar entre seções. |
| **Problemas de SEO/Findability**| O formato SPA é ruim para rastreabilidade e indexação (SEO). O Lovable não é ideal para websites grandes onde o tráfego orgânico é crucial. |
| **Função Ideal** | O Lovable é melhor utilizado para **protótipos funcionais rápidos** ou **landing pages únicas**, onde o SEO profundo não é a prioridade inicial. |
| **O Limite da Estabilidade** | Após ~300 mensagens, o tempo gasto debugando pode superar o progresso. Este é o ponto para refatorar ou migrar para um ambiente de código mais controlado. |

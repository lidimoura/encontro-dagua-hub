from fastapi import FastAPI
from supabase import create_client, Client
import os
import pathlib
import vertexai
from google.cloud import discoveryengine_v1alpha as discoveryengine
from vertexai.preview.generative_models import GenerativeModel

# Carrega as credenciais do Supabase a partir das variáveis de ambiente
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# --- NOVA CONFIGURAÇÃO GOOGLE CLOUD ---
PROJECT_ID = "gen-lang-client-0133480655"
LOCATION = "us-east4" # Região do seu RAG Corpus
RAG_CORPUS_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/6917529027641081856"

# Inicializa o Vertex AI (apenas uma vez, quando a API inicia)
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Inicializa os clientes das APIs (apenas uma vez)
rag_client = discoveryengine.RagServiceClient()
gemini_model = GenerativeModel("gemini-pro")

# Inicializa o cliente Supabase
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Encontro D'Água Hub API")

@app.get("/")
def health_check():
    """Verifica se a API está online e se a conexão com o Supabase foi estabelecida."""
    if supabase:
        return {"status": "A ignição funcionou!", "supabase_status": "Conectado"}
    else:
        return {"status": "A ignição funcionou!", "supabase_status": "Credenciais do Supabase não configuradas"}

def retrieve_rag_contexts(query_text: str) -> list[str]:
    """Usa a API do RAG Engine para buscar contextos relevantes."""
    request = discoveryengine.RetrieveContextsRequest(
        parent=RAG_CORPUS_RESOURCE_NAME,
        query=discoveryengine.RagQuery(text=query_text),
    )
    try:
        response = rag_client.retrieve_contexts(request=request)
        contexts = [context.chunk.chunk_data.text for context in response.contexts]
        print(f"✅ {len(contexts)} contextos encontrados pelo RAG Engine.")
        return contexts
    except Exception as e:
        print(f"❌ Erro ao buscar contextos no RAG Engine: {e}")
        return []

def generate_gemini_response(user_query: str, retrieved_contexts: list[str]) -> str:
    """Gera uma resposta com Gemini, usando os contextos do RAG."""
    if retrieved_contexts:
        context_str = "\n\n".join(retrieved_contexts)
        prompt = f"""
        Você é um assistente especialista do "Encontro D'Água Hub".
        Use os seguintes trechos de contexto para responder à pergunta do usuário.
        Responda de forma concisa e direta, baseando-se exclusivamente nas informações dos documentos.
        Se a resposta não estiver no contexto, diga "Com base no meu conhecimento atual, não tenho a resposta para isso."

        Contexto:
        ---
        {context_str}
        ---

        Pergunta do Usuário: {user_query}
        """
    else:
        prompt = f"""
        Você é um assistente especialista do "Encontro D'Água Hub".
        Nenhum contexto específico foi encontrado para esta pergunta.
        Responda à pergunta do usuário usando seu conhecimento geral e mencione que a resposta não se baseia em documentos específicos.

        Pergunta do Usuário: {user_query}
        """
    try:
        response = gemini_model.generate_content(prompt)
        print("✅ Resposta gerada pelo Gemini.")
        return response.text
    except Exception as e:
        print(f"❌ Erro ao gerar resposta com o Gemini: {e}")
        return "Desculpe, ocorreu um erro ao tentar gerar a resposta."

def select_specialist_or_get_answer(user_query: str) -> str:
    """
    Usa o 'Gem Gerente' para decidir o próximo passo:
    1. Responder diretamente (se for uma pergunta sobre o Hub).
    2. Criar um plano de ação (se for um novo projeto).
    3. Rotear para um especialista (se for uma tarefa pontual).
    """
    print(f"🤖 Gem Gerente está analisando a pergunta: '{user_query}'")
    try:
        # Carrega o "DNA" do Gem Gerente
        with open(pathlib.Path("specs/gem_gerente_v1.md"), "r", encoding="utf-8") as f:
            manager_prompt_template = f.read()

        # O prompt agora é mais aberto, instruindo o Gem a seguir seu blueprint.
        prompt = f"""
        {manager_prompt_template}

        ---
        Pergunta do Usuário a ser analisada: "{user_query}"
        ---
        """

        response = gemini_model.generate_content(prompt)
        manager_response = response.text.strip()
        print(f"✅ Resposta do Gem Gerente: '{manager_response}'")
        return manager_response

    except Exception as e:
        print(f"❌ Erro no Gem Gerente: {e}. Usando fallback.")
        return "Desculpe, o Gem Gerente está indisponível no momento. Tente novamente."

@app.post("/invoke_gem/{gem_id}")
def invoke_gem(gem_id: str, payload: dict):
    """
    Recebe uma pergunta, usa o RAG Engine para buscar contexto e o Gemini para gerar a resposta.
    Se o gem_id for 'gem_gerente_v1', ele primeiro determina o especialista ou a resposta direta.
    """
    pergunta = payload.get("pergunta")
    print(f"Recebido para o gem '{gem_id}': '{pergunta}'")

    available_gems = ["guia_tecnico_v1", "gem_briefing_v1", "gem_qa_v2.0", "gem_arquiteto_web_v1", "gem_onboarding_v1", "gem_revisor_entrega_v1", "gem_lovable_prompter_v1", "meta_gem_arquiteto_v1"]
    effective_gem_id = gem_id

    # --- LÓGICA DO GERENTE ---
    if gem_id == "gem_gerente_v1":
        manager_output = select_specialist_or_get_answer(pergunta)
        # Se a saída do gerente for um ID de especialista, nós o usamos.
        if manager_output in available_gems:
            effective_gem_id = manager_output
        # Se não for um ID, é uma resposta direta ou um plano. Retornamos imediatamente.
        else:
            print("✅ Gem Gerente forneceu uma resposta direta. Retornando ao usuário.")
            # A lógica de salvar no Supabase pode ser adicionada aqui se desejado
            return {"resposta": manager_output}

    try:
        # 1. Buscar contextos no RAG Engine
        contexts = retrieve_rag_contexts(pergunta)

        # 2. Gerar resposta com Gemini usando os contextos
        resposta_gem = generate_gemini_response(pergunta, contexts) # A geração da resposta final ainda é genérica

        # 3. Salvar log no Supabase (sem alterações)
        if supabase:
            try:
                supabase.table('gem_logs').insert({
                    "id_gem": gem_id,
                    "pergunta_usuario": pergunta,
                    "resumo_resposta_gem": resposta_gem
                }).execute()
            except Exception as e:
                print(f"Erro ao salvar log no Supabase: {e}")

        # Adiciona um cabeçalho para sabermos qual Gem respondeu
        if gem_id == "gem_gerente_v1":
            resposta_final = f"**Respondendo como `{effective_gem_id}`:**\n\n{resposta_gem}"
            return {"resposta": resposta_final}
        else:
            return {"resposta": resposta_gem}

    except Exception as e:
        print(f"Ocorreu um erro inesperado no invoke_gem: {e}")
        return {"resposta": f"Desculpe, ocorreu um erro ao processar sua pergunta. Detalhes: {e}"}
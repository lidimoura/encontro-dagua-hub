from fastapi import FastAPI
from supabase import create_client, Client
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- CONFIGURAÇÃO INICIAL ---
# Carrega as chaves de API a partir das variáveis de ambiente (serão injetadas pelo Cloud Run)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicializa o cliente Supabase
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- INICIALIZAÇÃO DOS SERVIÇOS DE IA (OpenAI + LangChain) ---
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# --- CARREGAMENTO E PROCESSAMENTO DA BASE DE CONHECIMENTO (RAG) ---
def carregar_e_processar_documentos():
    """
    Carrega todos os documentos .md das pastas 'specs' e 'base_conhecimento',
    divide-os em pedaços e os armazena em um banco de dados vetorial em memória (Chroma).
    Retorna um "retriever" que pode ser usado para buscar informações.
    """
    print("Iniciando carregamento da base de conhecimento...")
    # Carrega tanto os specs dos gems quanto a base de conhecimento geral
    loader_specs = DirectoryLoader('specs/', glob="**/*.md", loader_cls=TextLoader, show_progress=True)
    loader_base = DirectoryLoader('base_conhecimento/', glob="**/*.md", loader_cls=TextLoader, show_progress=True)
    documentos = loader_specs.load() + loader_base.load()
    print(f"✅ {len(documentos)} documentos carregados.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    textos = text_splitter.split_documents(documentos)
    print(f"📄 Documentos divididos em {len(textos)} pedaços.")

    # Cria o banco de dados vetorial em memória
    vector_db = Chroma.from_documents(textos, embeddings)
    print("✅ Banco de dados vetorial criado em memória.")
    return vector_db.as_retriever()

app = FastAPI(title="Encontro D'Água Hub API (OpenAI Edition)")
db_retriever = carregar_e_processar_documentos()

@app.get("/")
def health_check():
    """Verifica se a API está online e se a conexão com o Supabase foi estabelecida."""
    if supabase:
        return {"status": "API Encontro D'Água (OpenAI) no ar!", "supabase_status": "Conectado"}
    else:
        return {"status": "API Encontro D'Água (OpenAI) no ar!", "supabase_status": "Credenciais do Supabase não configuradas"}

def select_specialist_or_get_answer(user_query: str) -> str:
    """
    Usa o 'Gem Gerente' para decidir o próximo passo.
    """
    print(f"🤖 Gem Gerente está analisando a pergunta: '{user_query}'")
    try:
        # Carrega o "DNA" do Gem Gerente
        with open("specs/gem_gerente_v1.md", "r", encoding="utf-8") as f:
            manager_prompt_template = f.read()

        # Usa o LangChain para executar o prompt do gerente sem RAG
        prompt = PromptTemplate(template=manager_prompt_template, input_variables=["question"])
        chain = prompt | llm
        response = chain.invoke({"question": user_query})
        manager_response = response.content.strip()
        print(f"✅ Resposta do Gem Gerente: '{manager_response}'")
        return manager_response

    except Exception as e:
        print(f"❌ Erro no Gem Gerente: {e}. Usando fallback.")
        return "Desculpe, o Gem Gerente está temporariamente indisponível."

@app.post("/invoke_gem/{gem_id}")
def invoke_gem(gem_id: str, payload: dict):
    """
    Recebe uma pergunta, usa o RAG para buscar contexto e a OpenAI para gerar a resposta.
    """
    pergunta = payload.get("pergunta")
    print(f"Recebido para o gem '{gem_id}': '{pergunta}'")

    available_gems = ["guia_tecnico_v1", "gem_briefing_v1", "gem_qa_v2.0", "gem_arquiteto_web_v1", "gem_onboarding_v1", "gem_revisor_entrega_v1", "gem_lovable_prompter_v1", "meta_gem_arquiteto_v1"]

    # --- LÓGICA DO GERENTE ---
    if gem_id == "gem_gerente_v1":
        manager_output = select_specialist_or_get_answer(pergunta)
        if manager_output in available_gems:
            gem_id = manager_output # O gerente escolheu um especialista, então usamos esse ID
        else:
            print("✅ Gem Gerente forneceu uma resposta direta. Retornando ao usuário.")
            return {"resposta": manager_output}

    try:
        # Carrega o "DNA" do Gem especialista selecionado
        with open(f"specs/{gem_id}.md", "r", encoding="utf-8") as f:
            dna_do_gem = f.read()

        # Monta o prompt final para o RAG
        prompt_template = dna_do_gem + """

        Contexto: {context}
        Pergunta: {question}

        Sua Resposta:"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

        # Cria e executa a cadeia de RAG
        qa_chain = RetrievalQA.from_chain_type(
            llm, retriever=db_retriever, return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        resultado = qa_chain.invoke({"query": pergunta})
        resposta_gem = resultado["result"]

        if supabase:
            try:
                supabase.table('gem_logs').insert({
                    "id_gem": gem_id,
                    "pergunta_usuario": pergunta,
                    "resumo_resposta_gem": resposta_gem
                }).execute()
            except Exception as e:
                print(f"Erro ao salvar log no Supabase: {e}")

        return {"resposta": resposta_gem}

    except Exception as e:
        print(f"Ocorreu um erro inesperado no invoke_gem: {e}")
        return {"resposta": f"Desculpe, ocorreu um erro ao processar sua pergunta com o Gem '{gem_id}'."}
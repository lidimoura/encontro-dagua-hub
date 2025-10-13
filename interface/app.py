import streamlit as st
import os
import uuid
from supabase import create_client, Client

# IMPORTS DA STACK DE IA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- 1. CONFIGURAÇÃO GERAL DO HUB ---
CAMINHO_DO_CONHECIMENTO = "base_conhecimento/stack_atual_v3.md"
MEMORY_TABLE_NAME = "chat_memory"
LLM_MODEL = "gpt-4o-mini"
PROJECT_CONTEXT_TABLE_NAME = "project_context" # NOVO

# --- CONFIGURAÇÃO DOS AGENTES ---
AGENTE_GERENTE_ID = "agente_gerente_v4.1"
ESPECIALISTAS_IDS = [
    "agente_arquiteto_web_v2.2",
    "agente_qa_v2.3",
    "agente_onboarding_v2.2",
    "agente_briefing_v2.2",
    "agente_tecnico_v2",
    "agente_arquiteto_ia_v2",
    "agente_lovable_prompter_v2",
    "agente_revisor_entrega_v2",
    "agente_documentador_v2",
    "meta_agente_arquiteto_v2.1",
    "agente_projetos_v2",
    "agente_formatador_testes_v2",
]

# --- 2. CONFIGURAÇÃO DE SECRETS E SUPABASE ---
@st.cache_resource
def init_supabase_client() -> Client:
    try:
        url: str = st.secrets["SUPABASE_URL"]
        key: str = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar com Supabase: {e}")
        return None
supabase: Client = init_supabase_client()

# --- GESTÃO DE SESSÃO ---
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "project_id" not in st.session_state:
    st.session_state["project_id"] = ""
if "project_context" not in st.session_state:
    st.session_state["project_context"] = {}
current_session_id = st.session_state["session_id"]

# --- FUNÇÕES DE MEMÓRIA (CHAT E PROJETO) ---
def get_chat_history(session_id: str) -> list[dict]:
    if supabase:
        response = supabase.table(MEMORY_TABLE_NAME).select("role, content").eq("session_id", session_id).order("created_at", desc=False).execute()
        return response.data
    return []

def add_message_to_history(session_id: str, role: str, content: str):
    if supabase:
        data = {"session_id": session_id, "role": role, "content": content}
        supabase.table(MEMORY_TABLE_NAME).insert(data).execute()

# NOVO: Função para buscar o contexto de longo prazo do projeto
def get_project_context(project_id: str) -> dict:
    if supabase and project_id:
        try:
            response = supabase.table(PROJECT_CONTEXT_TABLE_NAME).select("context_key, context_content").eq("project_id", project_id).execute()
            return {item['context_key']: item['context_content'] for item in response.data}
        except Exception as e:
            st.error(f"Erro ao buscar contexto do projeto: {e}")
    return {}

def format_history_for_llm(messages: list[dict]) -> str:
    history_str = ""
    for msg in messages:
        content = msg['content'].split(':', 1)[-1].strip() if msg['role'] == 'assistant' and ':' in msg['content'] else msg['content']
        if msg["role"] == "user": history_str += f"HUMANO: {content}\n"
        elif msg["role"] == "assistant": history_str += f"ASSISTENTE: {content}\n"
    return history_str

# --- 3. CORE DE IA RAG ---
@st.cache_resource
def carregar_vector_store():
    if not os.path.exists(CAMINHO_DO_CONHECIMENTO):
        st.error(f"Arquivo de conhecimento não encontrado: {CAMINHO_DO_CONHECIMENTO}")
        return None
    try:
        loader = UnstructuredFileLoader(CAMINHO_DO_CONHECIMENTO)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        st.error(f"Erro ao carregar o RAG: {e}")
        return None
vector_store = carregar_vector_store()
retriever = vector_store.as_retriever() if vector_store else None
llm = ChatOpenAI(model=LLM_MODEL, temperature=0.5)

# --- 4. LÓGICA DE INVOCAÇÃO DOS AGENTES ---
def invoke_agente(agente_id: str, pergunta: str, history_str: str = ""):
    if not retriever:
        return "Erro: Sistema de conhecimento (RAG) não inicializado."
    
    caminho_do_dna = f"specs/{agente_id}.md"
    try:
        with open(caminho_do_dna, 'r', encoding='utf-8') as f:
            dna_do_agente = f.read()
    except FileNotFoundError:
        return f"Erro: Agente com ID '{agente_id}' não encontrado em {caminho_do_dna}."

    # ATUALIZADO: Lógica para injetar o contexto do projeto
    project_context_str = ""
    if "project_context" in st.session_state and st.session_state["project_context"]:
        project_context_str += "\n\n--- CONTEXTO GERAL DO PROJETO (MEMÓRIA DE LONGO PRAZO) ---\n"
        for key, value in st.session_state["project_context"].items():
            project_context_str += f"### Documento: {key.replace('_', ' ').title()}\n{value}\n\n"
    
    prompt_template = (
        dna_do_agente + 
        project_context_str + 
        ("\n\n--- HISTÓRICO DA CONVERSA RECENTE ---\n" + history_str + "\n\n" if history_str else "\n\n") + 
        "--- TAREFA ATUAL ---\nContexto Relevante do RAG: {context}\nPergunta do Usuário: {question}\n\nSua Resposta:"
    )
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    resultado = qa_chain.invoke({"query": pergunta})
    return resultado["result"]

def processar_orquestrador(pergunta_usuario: str, history_str: str):
    DELEGATION_MARKER = "DELEGAR:"
    decisao_bruta = invoke_agente(agente_id=AGENTE_GERENTE_ID, pergunta=pergunta_usuario, history_str=history_str)
    if isinstance(decisao_bruta, str) and DELEGATION_MARKER in decisao_bruta.upper():
        try:
            agente_selecionado = decisao_bruta.split(DELEGATION_MARKER)[1].strip().split()[0].lower().rstrip('.')
            if agente_selecionado in ESPECIALISTAS_IDS:
                st.info(f"Gerente decidiu: Roteando para o **{agente_selecionado}**...")
                resposta_final = invoke_agente(agente_id=agente_selecionado, pergunta=pergunta_usuario, history_str=history_str)
                return resposta_final, agente_selecionado
            else:
                return f"(Alerta: O Gerente tentou delegar para um agente inválido: '{agente_selecionado}'. Assumindo a resposta.)\n{decisao_bruta}", AGENTE_GERENTE_ID
        except Exception:
            return decisao_bruta, AGENTE_GERENTE_ID
    else:
        return decisao_bruta, AGENTE_GERENTE_ID

# --- 5. LOOP PRINCIPAL DO STREAMLIT (INTERFACE) ---
def formatar_nome_agente_para_exibicao(agente_id: str) -> str:
    if agente_id == AGENTE_GERENTE_ID:
        return "Gerente Padrão (Guia)"
    return agente_id.replace("agente_", "").replace("_", " ").split(' v')[0].title()

def chat_interface():
    st.set_page_config(page_title="🌀 Encontro D'Água Hub", layout="wide")
    st.title("🌀 Encontro D'Água Hub - Orquestrador de Soluções")
    
    if not supabase or not vector_store:
        st.error("O Hub não pôde inicializar. Verifique conexões.")
        return

    with st.sidebar:
        st.subheader("Controles do Hub (Arquiteta)")
        st.write(f"ID da Sessão: `{current_session_id[:8]}...`")

        # NOVO: Painel para carregar o Contexto do Projeto
        st.subheader("Memória de Projeto")
        project_id_input = st.text_input(
            "ID do Projeto Ativo:", 
            st.session_state.get("project_id", ""),
            help="Ex: 'bmd-synk'"
        )
        if st.button("Carregar Contexto"):
            st.session_state["project_id"] = project_id_input
            with st.spinner(f"Buscando contexto para '{project_id_input}'..."):
                st.session_state["project_context"] = get_project_context(project_id_input)
            if st.session_state["project_context"]:
                st.success(f"Contexto carregado para '{project_id_input}'!")
            else:
                st.warning(f"Nenhum contexto encontrado para '{project_id_input}'.")
        
        if st.session_state.get("project_id"):
            st.info(f"Projeto ativo: **{st.session_state['project_id']}**")

        st.divider()
        
        st.subheader("Controles de Execução")
        agente_override = st.selectbox(
            "Forçar Especialista (Override):",
            [AGENTE_GERENTE_ID] + ESPECIALISTAS_IDS,
            format_func=formatar_nome_agente_para_exibicao
        )
        
        if st.button("Limpar Histórico de Conversa"):
            if supabase:
                supabase.table(MEMORY_TABLE_NAME).delete().eq("session_id", current_session_id).execute()
                st.rerun()

    raw_history = get_chat_history(current_session_id)
    for message in raw_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Pergunte ao Hub..."):
        history_for_llm = format_history_for_llm(raw_history)
        add_message_to_history(current_session_id, "user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Hub pensando..."):
            speaking_agent_id = AGENTE_GERENTE_ID
            if agente_override != AGENTE_GERENTE_ID:
                resposta_final = invoke_agente(agente_id=agente_override, pergunta=prompt, history_str=history_for_llm)
                speaking_agent_id = agente_override
            else:
                resposta_final, speaking_agent_id = processar_orquestrador(prompt, history_for_llm)
        
        labeled_resposta_final = f"**{speaking_agent_id.upper()}:** {resposta_final}"
        add_message_to_history(current_session_id, "assistant", labeled_resposta_final)
        
        st.rerun()

if __name__ == "__main__":
    chat_interface()

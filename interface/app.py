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

# --- 1. CONFIGURAÇÃO DE SECRETS E SUPABASE (MEMÓRIA) ---

MEMORY_TABLE_NAME = "chat_memory" 

@st.cache_resource
def init_supabase_client() -> Client:
    """Inicializa e armazena o cliente Supabase em cache."""
    try:
        url: str = st.secrets["SUPABASE_URL"]
        key: str = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar com Supabase. Verifique os secrets: {e}")
        return None

supabase: Client = init_supabase_client()

# --- GESTÃO DE SESSÃO (UUID) ---
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

current_session_id = st.session_state["session_id"]

# --- FUNÇÕES DE MEMÓRIA PERSISTENTE ---

def get_chat_history(session_id: str) -> list[dict]:
    """Recupera o histórico de mensagens da tabela chat_memory."""
    if supabase:
        response = supabase.table(MEMORY_TABLE_NAME).select("role, content").eq("session_id", session_id).order("created_at", desc=False).execute()
        return response.data
    return []

def add_message_to_history(session_id: str, role: str, content: str):
    """Adiciona uma nova mensagem ao histórico do chat_memory."""
    if supabase:
        data = {
            "session_id": session_id,
            "role": role, # 'user' ou 'assistant'
            "content": content
        }
        supabase.table(MEMORY_TABLE_NAME).insert(data).execute()

# NOVO: Função que formata o histórico para ser usado no Prompt
def format_history_for_llm(messages: list[dict]) -> str:
    """Converte o histórico do Supabase para um formato de string que o LLM pode usar."""
    history_str = ""
    for msg in messages:
        # Remove o prefixo do Agente para o LLM não se confundir
        content = msg['content'].split(':', 1)[-1].strip() if msg['role'] == 'assistant' and ':' in msg['content'] else msg['content']
        
        if msg["role"] == "user":
            history_str += f"HUMANO: {content}\n"
        elif msg["role"] == "assistant":
            history_str += f"ASSISTENTE: {content}\n"
    return history_str

# --- 2. CORE DE IA RAG (OpenAI/Chroma) ---

CAMINHO_DO_CONHECIMENTO = "base_conhecimento/stack_atual_v2.md" 
LLM_MODEL = "gpt-3.5-turbo"

@st.cache_resource
def carregar_vector_store():
    """Carrega o Vector Store usando Chroma e OpenAI Embeddings."""
    
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

# --- LÓGICA DE INVOCAÇÃO DOS AGENTES (ESPECIALISTAS) ---

# CORREÇÃO: invoke_agente agora aceita o history_str
def invoke_agente(agente_id: str, pergunta: str, history_str: str = ""):
    """
    Função que busca o DNA do Agente (Especialista), executa a cadeia RAG/QA e injeta o histórico.
    """
    if not retriever:
         return "Erro: Sistema de conhecimento (RAG) não inicializado. Não é possível invocar o Agente."
         
    caminho_do_dna = f"specs/{agente_id}.md"
    
    try:
        with open(caminho_do_dna, 'r', encoding='utf-8') as f:
            dna_do_agente = f.read()
    except FileNotFoundError:
        return f"Erro: Agente com ID '{agente_id}' não encontrado em {caminho_do_dna}. Verifique se o nome do arquivo corresponde ao ID no código."

    # CORREÇÃO: Injeta o histórico da conversa no Prompt Template
    prompt_template = dna_do_agente + (
        "\n\nHistórico da Conversa:\n" + history_str + "\n\n" if history_str else "\n\n"
    ) + "Contexto: {context}\nPergunta: {question}\n\nSua Resposta:"
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    resultado = qa_chain.invoke({"query": pergunta})
    return resultado["result"]


# CORREÇÃO: processar_orquestrador agora aceita o history_str
def processar_orquestrador(pergunta_usuario: str, history_str: str, orquestrador_id: str = "agente_gerente_v3.3"):
    """
    Controla o fluxo principal: O Agente Gerente decide se responde ou delega, usando o histórico.
    """
    DELEGATION_MARKER = "DELEGAR:" 
    
    # CORREÇÃO: Passa o histórico na invocação
    decisao_bruta = invoke_agente(agente_id=orquestrador_id, pergunta=pergunta_usuario, history_str=history_str)
    
    if isinstance(decisao_bruta, str) and DELEGATION_MARKER in decisao_bruta.upper():
        try:
            agente_selecionado = decisao_bruta.split(DELEGATION_MARKER)[1].strip()
            agente_selecionado = agente_selecionado.replace(".", "").lower() 
            
            st.info(f"Gerente decidiu: Roteando para o **{agente_selecionado}**...")
            
            # CORREÇÃO: Passa o histórico na delegação
            resposta_final = invoke_agente(agente_id=agente_selecionado, pergunta=pergunta_usuario, history_str=history_str)
            return resposta_final, agente_selecionado 
        except Exception:
            return decisao_bruta, orquestrador_id
    
    else:
        return decisao_bruta, orquestrador_id 


# --- 3. LOOP PRINCIPAL DO STREAMLIT (INTERFACE) ---

def chat_interface():
    
    # BRANDING FINAL: Emojis e títulos
    st.set_page_config(page_title="🌀 Encontro D'Água Hub", layout="wide")
    st.title("🌀 Encontro D'Água Hub - Orquestrador de Soluções")
    
    if not vector_store:
        st.error("O Hub não pôde inicializar o Vector Store. Por favor, verifique os logs de erro ou o caminho do arquivo de conhecimento.")
        return

    current_session_id = st.session_state["session_id"]
    
    # ID: AGENTE_GERENTE_V3.3
    AGENTE_GERENTE_ID = "agente_gerente_v3.3" 
    
    # LISTA COMPLETA DOS 9 ESPECIALISTAS
    available_agentes = [
        "agente_arquiteto_web_v1", "agente_briefing_v1.1", "agente_documentador_v1", 
        "agente_lovable_prompter_v1", "agente_onboarding_v1", "agente_qa_v2", 
        "agente_revisor_entrega_v1", "guia_tecnico_v1", "meta_agente_arquiteto_v1"
    ]
    
    with st.sidebar:
        st.subheader("Controles do Hub (Arquiteta)")
        st.write(f"ID da Sessão: `{current_session_id[:8]}...`")
        
        agente_override = st.selectbox(
            "Forçar Especialista (Override):", 
            [AGENTE_GERENTE_ID] + available_agentes,
            format_func=lambda x: f"Gerente Padrão" if x == AGENTE_GERENTE_ID else x.replace("agente_", "").replace("_v1", "").replace("_v2", "").replace("v3", "").replace("v3.1", "").replace("meta_", "").replace(".", "").upper()
        )
        
        if st.button("Limpar Histórico de Conversa (Memória)"):
            supabase.table(MEMORY_TABLE_NAME).delete().eq("session_id", current_session_id).execute()
            st.rerun()

    # --- 4. EXIBIÇÃO DO HISTÓRICO (Memória) ---
    raw_history = get_chat_history(current_session_id)
    
    for message in raw_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- 5. TRATAMENTO DE NOVA PERGUNTA (Loop Principal) ---
    if prompt := st.chat_input("Pergunte ao Hub..."):
        
        # CORREÇÃO: Formata o histórico do Supabase para o LLM
        history_for_llm = format_history_for_llm(raw_history)
        
        # A. Salva e Exibe a Pergunta do Usuário
        add_message_to_history(current_session_id, "user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Hub pensando..."):
            
            speaking_agent_id = AGENTE_GERENTE_ID
            
            if agente_override != AGENTE_GERENTE_ID:
                # 1. ROTA DE OVERRIDE
                # CORREÇÃO: Passa o histórico na invocação
                resposta_final = invoke_agente(agente_id=agente_override, pergunta=prompt, history_str=history_for_llm)
                speaking_agent_id = agente_override
            else:
                # 2. ROTA DO GERENTE
                # CORREÇÃO: Passa o histórico no processamento
                resposta_final, agente_falante_da_resposta = processar_orquestrador(prompt, history_for_llm)
                speaking_agent_id = agente_falante_da_resposta
        
        # B. CORREÇÃO DE UX E SUPABASE: Adiciona o ID do Agente falante à mensagem
        labeled_resposta_final = f"**{speaking_agent_id.upper()}:** {resposta_final}"
        
        # C. Salva e Exibe a Resposta do Hub
        add_message_to_history(current_session_id, "assistant", labeled_resposta_final)
        
        with st.chat_message("assistant"):
            st.markdown(labeled_resposta_final)
            
        st.rerun() 

# --- EXECUÇÃO FINAL ---
if __name__ == "__main__":
    chat_interface()

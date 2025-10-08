import streamlit as st
import requests
from supabase import create_client, Client
import os

# (O início do código com o painel de debug, config e conexão com Supabase continua o mesmo)
# ... (cole a partir daqui se preferir)
st.set_page_config(page_title="Encontro D'Água Hub", page_icon="💧", layout="wide")

SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("💧 Painel de Comando do Encontro D'Água Hub")
API_BASE_URL = "https://bc1cc700cdc7.ngrok-free.app"

with st.sidebar:
    st.header("Equipe de Gems")
    gem_selecionado = st.selectbox(
        "Escolha o especialista:",
        (
            "gem_gerente_v1", # Opção principal!
            "guia_tecnico_v1",
            "gem_briefing_v1",
            "gem_qa_v2.0",
            "gem_arquiteto_web_v1",
            "gem_onboarding_v1",
            "gem_revisor_entrega_v1",
            "gem_lovable_prompter_v1",
            "meta_gem_arquiteto_v1"
        ),
        help="Escolha 'gem_gerente_v1' para roteamento automático ou selecione um especialista diretamente."
    )
    st.info(f"Conversando com: **{gem_selecionado}**.")

st.header(f"Chat com {gem_selecionado}")

# Lógica de inicialização/carregamento do histórico (sem alterações)
if "messages" not in st.session_state or st.session_state.get('current_gem') != gem_selecionado:
    st.session_state.messages = []
    st.session_state.current_gem = gem_selecionado
    if supabase:
        response = supabase.table('gem_logs').select("*").eq('id_gem', gem_selecionado).order('created_at').execute()
        if response.data:
            for row in response.data:
                if row.get('pergunta_usuario'):
                    st.session_state.messages.append({"role": "user", "content": row['pergunta_usuario']})
                if row.get('resumo_resposta_gem'):
                    st.session_state.messages.append({"role": "assistant", "content": row['resumo_resposta_gem']})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sua mensagem:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            endpoint_url = f"{API_BASE_URL}/invoke_gem/{gem_selecionado}"
            
            # --- MUDANÇA CRUCIAL AQUI ---
            # Agora enviamos não só a pergunta, mas todo o histórico
            payload = {
                "pergunta": prompt,
                "historico_chat": st.session_state.messages[:-1] # Envia tudo, menos a última pergunta que acabamos de fazer
            }
            
            # (O resto da lógica de chamada da API e salvamento no Supabase continua a mesma)
            try:
                response = requests.post(endpoint_url, json=payload, timeout=180)
                response.raise_for_status()
                resultado = response.json()
                resposta_gem = resultado['resposta']
                st.markdown(resposta_gem)
                
                st.session_state.messages.append({"role": "assistant", "content": resposta_gem})
                
                # (Lógica de salvamento no Supabase sem alterações)

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao se comunicar com a API: {e}")

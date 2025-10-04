import streamlit as st
import requests
import json
from supabase import create_client, Client
import os

# --- PAINEL DE DEBUG (Temporário) ---
with st.expander("🕵️‍♀️ Painel de Detetive de Segredos"):
    st.write("Verificando se os segredos do Supabase foram carregados do ambiente do Streamlit Cloud:")

    # Pega os valores dos segredos
    url_secret = st.secrets.get("SUPABASE_URL")
    key_secret = st.secrets.get("SUPABASE_KEY")

    # Verifica e exibe o status
    if url_secret:
        st.success("✅ Segredo SUPABASE_URL encontrado!")
    else:
        st.error("❌ ERRO: Segredo SUPABASE_URL NÃO encontrado!")

    if key_secret:
        st.success("✅ Segredo SUPABASE_KEY encontrado!")
    else:
        st.error("❌ ERRO: Segredo SUPABASE_KEY NÃO encontrado!")

# --- O RESTO DO CÓDIGO CONTINUA IGUAL ---

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Encontro D'Água Hub",
    page_icon="💧",
    layout="wide"
)

# --- CONEXÃO COM O SUPABASE ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CABEÇALHO E URL DA API ---
st.title("💧 Painel de Comando do Encontro D'Água Hub")
API_BASE_URL = "https://encontro-dagua-hub-api-192934687919.southamerica-east1.run.app"

# (O resto do código do chat e da barra lateral continua aqui, sem alterações)
# --- BARRA LATERAL PARA SELEÇÃO DE GEMS ---
with st.sidebar:
    st.header("Equipe de Gems")
    gem_selecionado = st.selectbox(
        "Escolha o especialista:",
        ("guia_tecnico_v1", "gem_qa_v1")
    )
    st.info(f"Conversando com: **{gem_selecionado}**.")

# --- LÓGICA DO CHAT COM MEMÓRIA ---
st.header(f"Chat com {gem_selecionado}")

if "messages" not in st.session_state:
    st.session_state.messages = []

if supabase and not st.session_state.messages:
    try:
        response = supabase.table('gem_logs').select("*").eq('id_gem', gem_selecionado).order('created_at').execute()
        if response.data:
            for row in response.data:
                if row.get('pergunta_usuario'):
                    st.session_state.messages.append({"role": "user", "content": row['pergunta_usuario']})
                if row.get('resumo_resposta_gem'):
                    st.session_state.messages.append({"role": "assistant", "content": row['resumo_resposta_gem']})
    except Exception as e:
        st.error(f"Erro ao buscar histórico do Supabase: {e}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sua mensagem:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if supabase:
        try:
            supabase.table('gem_logs').insert({
                "id_gem": gem_selecionado, 
                "pergunta_usuario": prompt,
                "id_projeto": "hub_interface_v1"
            }).execute()
        except Exception as e:
            st.error(f"Erro ao salvar pergunta no Supabase: {e}")

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            endpoint_url = f"{API_BASE_URL}/invoke_gem/{gem_selecionado}"
            payload = {"pergunta": prompt}
            try:
                response = requests.post(endpoint_url, json=payload, timeout=180)
                response.raise_for_status()
                resultado = response.json()
                resposta_gem = resultado['resposta']
                st.markdown(resposta_gem)

                st.session_state.messages.append({"role": "assistant", "content": resposta_gem})

                if supabase:
                    try:
                        # A forma correta de atualizar a linha mais recente que corresponde à pergunta
                        supabase.table('gem_logs').update({"resumo_resposta_gem": resposta_gem}).eq("pergunta_usuario", prompt).is_("resumo_resposta_gem", "null").execute()
                    except Exception as e:
                        st.error(f"Erro ao atualizar resposta no Supabase: {e}")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao se comunicar com a API: {e}")
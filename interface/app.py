import streamlit as st
import requests
from supabase import create_client, Client
import os

# --- PAINEL DE DEBUG (Pode ser removido depois) ---
with st.expander("🕵️‍♀️ Painel de Detetive de Segredos"):
    url_secret = st.secrets.get("SUPABASE_URL") is not None
    key_secret = st.secrets.get("SUPABASE_KEY") is not None
    st.write(f"Segredo SUPABASE_URL encontrado: {'✅ Sim' if url_secret else '❌ Não'}")
    st.write(f"Segredo SUPABASE_KEY encontrado: {'✅ Sim' if key_secret else '❌ Não'}")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Encontro D'Água Hub", page_icon="💧", layout="wide")

# --- CONEXÃO COM O SUPABASE ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CABEÇALHO E URL DA API ---
st.title("💧 Painel de Comando do Encontro D'Água Hub")
API_BASE_URL = "https://encontro-dagua-hub-api-192934687919.southamerica-east1.run.app"

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Equipe de Gems")
    gem_selecionado = st.selectbox("Escolha o especialista:",
    ("guia_tecnico_v1", "gem_qa_v2.0", "gem_arquiteto_web_v1", "gem_onboarding_v1", "gem_revisor_entrega_v1", "gem_lovable_prompter_v1", "meta_gem_arquiteto_v1"))
    st.info(f"Conversando com: **{gem_selecionado}**.")

# --- LÓGICA DO CHAT COM MEMÓRIA ---
st.header(f"Chat com {gem_selecionado}")

# Lógica para carregar o histórico ao iniciar ou trocar de Gem
if "messages" not in st.session_state or st.session_state.get('current_gem') != gem_selecionado:
    st.session_state.messages = []
    st.session_state.current_gem = gem_selecionado
    if supabase:
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

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura a nova pergunta do usuário
if prompt := st.chat_input("Sua mensagem:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    new_log_id = None
    if supabase:
        try:
            # Insere a pergunta e pede o ID de volta
            insert_response = supabase.table('gem_logs').insert({
                "id_gem": gem_selecionado, 
                "pergunta_usuario": prompt,
                "id_projeto": "hub_interface_v1"
            }).execute()
            new_log_id = insert_response.data[0]['id']
        except Exception as e:
            st.error(f"Erro ao salvar pergunta no Supabase: {e}")
    
    # Chama a API e exibe a resposta
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
                
                # Atualiza a resposta no Supabase usando o ID
                if supabase and new_log_id:
                    try:
                        supabase.table('gem_logs').update({"resumo_resposta_gem": resposta_gem}).eq("id", new_log_id).execute()
                    except Exception as e:
                        st.error(f"Erro ao atualizar resposta no Supabase: {e}")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao se comunicar com a API: {e}")

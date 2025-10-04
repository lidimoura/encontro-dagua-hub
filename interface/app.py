import streamlit as st
import requests
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Encontro D'Água Hub",
    page_icon="💧",
    layout="wide"
)

# --- CABEÇALHO ---
st.title("💧 Painel de Comando do Encontro D'Água Hub")
st.caption("Converse com sua equipe de Gems especialistas.")

# --- URL BASE DA NOSSA API NO CLOUD RUN ---
API_BASE_URL = "https://encontro-dagua-hub-api-192934687919.southamerica-east1.run.app"

# --- BARRA LATERAL PARA SELEÇÃO DE GEMS (MUDANÇA 2 e 3) ---
with st.sidebar:
    st.header("Equipe de Gems")
    # Nossos especialistas. Quando "contratarmos" mais, é só adicionar a ID aqui!
    gem_selecionado = st.selectbox(
        "Escolha o especialista com quem deseja conversar:",
        ("guia_tecnico_v1", "gem_qa_v1")
    )
    st.info(f"Você está conversando com o **{gem_selecionado}**.")

# --- INTERFACE DO CHAT (MUDANÇA 4) ---
st.header(f"Chat com {gem_selecionado}")

prompt = st.text_input("Sua mensagem:", key="prompt_input")

if st.button("Enviar"):
    if prompt:
        with st.spinner(f"O {gem_selecionado} está pensando..."):
            # Monta a URL completa do endpoint dinamicamente
            endpoint_url = f"{API_BASE_URL}/invoke_gem/{gem_selecionado}"
            
            # Monta os dados para enviar para a API
            payload = {"pergunta": prompt}
            
            try:
                # Chamando nossa API FastAPI
                response = requests.post(endpoint_url, json=payload, timeout=180)
                response.raise_for_status()
                
                # Exibindo a resposta
                resultado = response.json()
                st.success("Resposta Recebida:")
                st.markdown(resultado['resposta'])

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao se comunicar com a API: {e}")
    else:
        st.warning("Por favor, digite uma mensagem.")
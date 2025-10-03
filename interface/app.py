import streamlit as st
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Encontro D'Água Hub",
    page_icon="💧",
    layout="wide"
)

# --- CABEÇALHO ---
st.title("💧 Encontro D'Água Hub")
st.caption("Seu painel de comando para a equipe de Gems")

# --- URL DA NOSSA API (O PONTO DE CONEXÃO) ---
API_URL = "https://encontro-dagua-hub-api-192934687919.southamerica-east1.run.app/ask_gem_tecnico"

# --- INTERFACE DO CHAT ---
st.subheader("Converse com seu Gem Guia Técnico")
prompt = st.text_input("Faça sua pergunta sobre o stack ou o projeto:", key="prompt_input")

if st.button("Enviar Pergunta"):
    if prompt:
        with st.spinner("O Gem está pensando..."):
            # Montando os dados para enviar para a API
            payload = {"pergunta": prompt}
            
            try:
                # Chamando nossa API FastAPI
                response = requests.post(API_URL, json=payload, timeout=120) # Timeout de 2 min
                response.raise_for_status()
                
                # Exibindo a resposta
                resultado = response.json()
                st.success("Resposta Recebida!")
                st.markdown(resultado['resposta'])

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao se comunicar com a API: {e}")
    else:
        st.warning("Por favor, digite uma pergunta.")
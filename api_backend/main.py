import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

# --- CONFIGURAÇÃO INICIAL ---
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("⚠️ Chave de API não encontrada.")

# --- CARREGAMENTO DO RAG v1.0 (SIMPLES E ROBUSTO) ---
def carregar_vector_store():
    # Voltamos a ler um único arquivo para garantir a estabilidade
    caminho_base = "base_conhecimento/stack_atual_v2.md"
    with open(caminho_base, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(conteudo)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)

    print("✅ Vector Store (versão estável) pronto!")
    return vector_store

# Carrega o conhecimento UMA VEZ quando a API inicia
vector_store = carregar_vector_store()
retriever = vector_store.as_retriever()
llm = GoogleGenerativeAI(model="models/gemini-flash-latest")

# --- API "GEM GERENTE" ---
app = FastAPI(title="Encontro D'Água Hub API")

class QueryRequest(BaseModel):
    pergunta: str

@app.post("/invoke_gem/{gem_id}")
def invoke_gem(gem_id: str, request: QueryRequest):
    caminho_da_receita = f"specs/{gem_id}.md"
    try:
        with open(caminho_da_receita, 'r', encoding='utf-8') as f:
            dna_do_gem = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Gem com id '{gem_id}' não encontrado.")

    prompt_template = dna_do_gem + """

    Contexto: {context}
    Pergunta: {question}

    Sua Resposta:"""

    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever,
        return_source_documents=True, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    resultado = qa_chain.invoke({"query": request.pergunta})
    return {"resposta": resultado["result"], "fontes": [doc.page_content for doc in resultado["source_documents"]]}

@app.get("/")
def health_check():
    return {"status": "API do Encontro D'Água Hub (v3.0 Estável) está no ar!"}
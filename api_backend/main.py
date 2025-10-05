import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# Importações COMPLETAS do LangChain
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import DirectoryLoader

# --- CONFIGURAÇÃO INICIAL DA CHAVE DE API ---
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("⚠️ Chave de API não encontrada. O deploy pode falhar se a variável de ambiente não estiver configurada.")

# --- CARREGAMENTO DO RAG v2.0 (LENDO A BIBLIOTECA INTEIRA NA INICIALIZAÇÃO) ---
def carregar_vector_store():
    loader = DirectoryLoader('base_conhecimento/', glob="**/*.md", show_progress=True)
    documentos = loader.load()
    print(f"Carregados {len(documentos)} documentos da base de conhecimento.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documentos)
    print(f"Total de {len(chunks)} chunks de conhecimento criados.")

    print("Gerando embeddings e criando o vector store...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)

    print("✅ Vector Store (versão completa) pronto!")
    return vector_store

# Carrega o conhecimento UMA VEZ quando a API inicia (o jeito profissional)
vector_store = carregar_vector_store()
retriever = vector_store.as_retriever()
llm = GoogleGenerativeAI(model="models/gemini-flash-latest")

# --- API "GEM GERENTE" ---
app = FastAPI(title="Encontro D'Áua Hub API")

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
    return {"status": "API do Encontro D'Água Hub (v4.0 Produção) está no ar!"}
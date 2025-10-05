import os
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# Importações do LangChain
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

# --- RECURSOS GLOBAIS (INICIALIZADOS VAZIOS) ---
# A carga pesada só acontecerá no primeiro request
vector_store = None
llm = None

app = FastAPI(title="Encontro D'Áua Hub API")

# --- FUNÇÃO DE CARGA "PREGUIÇOSA" (LAZY LOADING) ---
def carregar_recursos_de_ia():
    global vector_store, llm
    # Esta função só executa o código pesado UMA VEZ
    if vector_store is None:
        print("Iniciando a carga dos recursos de IA (RAG) pela primeira vez...")
        try:
            caminho_base = "base_conhecimento/stack_atual_v2.md"
            with open(caminho_base, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = text_splitter.split_text(conteudo)
            
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)
            llm = GoogleGenerativeAI(model="models/gemini-flash-latest")
            print("✅ Recursos de IA carregados com sucesso.")
        except Exception as e:
            print(f"❌ ERRO CRÍTICO AO CARREGAR RECURSOS DE IA: {e}")
            traceback.print_exc() # Imprime o erro detalhado nos logs
            raise e # Levanta o erro para parar o processo

# --- API "GEM GERENTE" ---
class QueryRequest(BaseModel):
    pergunta: str

@app.post("/invoke_gem/{gem_id}")
def invoke_gem(gem_id: str, request: QueryRequest):
    # Garante que os recursos de IA estão carregados antes de prosseguir
    try:
        carregar_recursos_de_ia()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao inicializar a IA: {str(e)}")

    # O resto da lógica continua a mesma
    caminho_da_receita = f"specs/{gem_id}.md"
    try:
        with open(caminho_da_receita, 'r', encoding='utf-8') as f:
            dna_do_gem = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Gem com id '{gem_id}' não encontrado.")

    retriever = vector_store.as_retriever()
    prompt_template = dna_do_gem + "\n\nContexto: {context}\nPergunta: {question}\n\nSua Resposta:"
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever,
        return_source_documents=True, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    resultado = qa_chain.invoke({"query": request.pergunta})
    return {"resposta": resultado["result"], "fontes": [doc.page_content for doc in resultado["source_documents"]]}

@app.get("/")
def health_check():
    return {"status": "API do Encontro D'Água Hub (v4.0 Debug) está no ar!"}
import os
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Importações do LangChain
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI

# --- CARREGAMENTO E CONFIGURAÇÃO INICIAL (O CORAÇÃO DO NOSSO RAG) ---

# Carregando a chave de API do ambiente 
def configurar_api_key():
    """Carrega a chave da API a partir de variáveis de ambiente ou Colab Secrets."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("🔑 Chave de API carregada das variáveis de ambiente.")
        genai.configure(api_key=api_key)
        return

    try:
        from google.colab import userdata
        api_key = userdata.get('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        print("🔑 Chave de API carregada do Colab Secrets.")
    except (ImportError, KeyError):
        raise ValueError("ERRO CRÍTICO: GOOGLE_API_KEY não encontrada. Configure-a como variável de ambiente.")

configurar_api_key()

# Caminho para nossa base de conhecimento (CORRIGIDO)
CAMINHO_BASE_CONHECIMENTO = "base_conhecimento/stack_atual.md"

# Esta função carrega e prepara nosso "índice de fichas" (Vector Store)
def carregar_vector_store():
    print("Carregando base de conhecimento...")
    with open(CAMINHO_BASE_CONHECIMENTO, 'r', encoding='utf-8') as f:
        conteudo_documento = f.read()
    
    print("Dividindo o documento em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    text_chunks = text_splitter.split_text(conteudo_documento)
    
    print("Criando embeddings e o vector store...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    print("✅ Vector Store pronto!")
    return vector_store

# Carregamos o vector store UMA VEZ quando a API inicia
vector_store = carregar_vector_store()

# --- DEFINIÇÃO DA API E SEUS ENDPOINTS ---

# Criando a aplicação FastAPI
app = FastAPI(title="Encontro D'Água Hub API")

# Definindo o formato da pergunta que vamos receber
class QueryRequest(BaseModel):
    pergunta: str

# Criando a cadeia de RAG
llm = GoogleGenerativeAI(model="gemini-1.0-pro")
retriever = vector_store.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
)

# Endpoint principal para fazer perguntas
@app.post("/ask_gem_tecnico")
def ask_question(request: QueryRequest):
    """
    Recebe uma pergunta e retorna a resposta do Gem Guia Técnico.
    """
    print(f"Recebida a pergunta: {request.pergunta}")
    
    # Invoca nosso Gem para obter a resposta
    resultado = qa_chain.invoke({"query": request.pergunta})
    
    print(f"Resposta gerada: {resultado['result']}")
    return {"resposta": resultado["result"]}

# Endpoint de "saúde" para verificar se a API está no ar
@app.get("/")
def health_check():
    return {"status": "API do Encontro D'Água Hub está no ar!"}

# --- BLOCO PARA EXECUÇÃO (PARA DEPLOY NO CLOUD RUN) ---

if __name__ == "__main__":
    import uvicorn

    # O Cloud Run define a variável de ambiente PORT. Usamos ela ou o padrão 8080.
    port = int(os.environ.get("PORT", 8080))
    
    # Rodamos o servidor Uvicorn. O host '0.0.0.0' é crucial para que o 
    # contêiner aceite conexões externas.
    uvicorn.run(app, host="0.0.0.0", port=port)

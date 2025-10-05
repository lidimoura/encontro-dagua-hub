import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional # <-- Importamos novas ferramentas de tipagem

# (O resto das importações do LangChain continuam as mesmas)
# ...

# (Configuração inicial e carregamento do RAG continuam os mesmos)
# ...

# --- API "GEM GERENTE" v3.0 com Memória ---
app = FastAPI(title="Encontro D'Água Hub API")

# --- MUDANÇA CRUCIAL AQUI ---
# Atualizamos nosso modelo de requisição para aceitar o histórico
class QueryRequest(BaseModel):
    pergunta: str
    historico_chat: Optional[List[Dict[str, str]]] = None # O histórico é uma lista opcional

# Função para formatar o histórico para o prompt
def formatar_historico(historico: List[Dict[str, str]]) -> str:
    if not historico:
        return ""
    
    chat_formatado = "\n\nHistórico da Conversa Anterior:\n"
    for msg in historico:
        role = "Você" if msg["role"] == "user" else "Gem"
        chat_formatado += f"- {role}: {msg['content']}\n"
    return chat_formatado

@app.post("/invoke_gem/{gem_id}")
def invoke_gem(gem_id: str, request: QueryRequest):
    print(f"Recebido pedido para o Gem: {gem_id}")
    
    caminho_da_receita = f"specs/{gem_id}.md"
    
    try:
        with open(caminho_da_receita, 'r', encoding='utf-8') as f:
            dna_do_gem = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Gem com id '{gem_id}' não encontrado.")

    # --- MUDANÇA CRUCIAL AQUI ---
    # Formatamos o histórico e o adicionamos ao prompt
    historico_formatado = formatar_historico(request.historico_chat)
    
    prompt_template = dna_do_gem + historico_formatado + """

    Contexto Relevante (Buscado na Base de Conhecimento): {context}
    Pergunta Atual do Usuário: {question}
    
    Sua Resposta:"""
    
    # (O resto da lógica da cadeia de RAG continua a mesma)
    from langchain.prompts import PromptTemplate
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    resultado = qa_chain.invoke({"query": request.pergunta})
    
    return {"resposta": resultado["result"], "fontes": [doc.page_content for doc in resultado["source_documents"]]}

@app.get("/")
def health_check():
    return {"status": "API do Encontro D'Água Hub (v3.0 Gerente com Memória) está no ar!"}

    
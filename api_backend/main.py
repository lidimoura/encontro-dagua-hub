from fastapi import FastAPI

app = FastAPI(title="Teste de Ignição do Hub")

@app.get("/")
def health_check():
    return {"status": "A ignição funcionou!"}
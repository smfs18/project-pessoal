# main.py

from fastapi import FastAPI
# Adicione esta importação
from fastapi.middleware.cors import CORSMiddleware
from app.routes import webhook
import uvicorn

app = FastAPI(
    title="ClinicAI Triage Agent",
    description="API para o agente de triagem da ClinicAI",
    version="1.0.0"
)

# --- INÍCIO DA ADIÇÃO PARA O CORS ---

# Lista de "origens" (endereços) que têm permissão para acessar nossa API.
# O asterisco "*" significa "qualquer um". É seguro para desenvolvimento local.
# O "null" é importante para permitir requisições de arquivos locais (file://).
origins = [
    "*",
    "null", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# --- FIM DA ADIÇÃO PARA O CORS ---


# Inclui as rotas definidas no arquivo webhook.py
app.include_router(webhook.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "ClinicAI Triage Agent is running."}

# Para executar o servidor localmente
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
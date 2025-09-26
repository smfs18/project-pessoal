from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from app.routes import webhook 
import uvicorn 


app = FastAPI(
    title="ClinicAI Triage Agent",
    description="API para o agente de triagem da ClinicAI",
    version="1.0.0"
)

origins = [
    "*",
    "null", 
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(webhook.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "ClinicAI Triage Agent is running."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.triage_agent import TriageAgent

router = APIRouter()
agent = TriageAgent()

class UserInput(BaseModel):
    session_id: str  # Pode ser o número de telefone ou um ID único do chat
    message: str

@router.post("/chat", tags=["Chat"])
async def handle_chat_message(user_input: UserInput):
    """
    Recebe uma mensagem do usuário e retorna a resposta do agente.
    """
    if not user_input.message or not user_input.session_id:
        raise HTTPException(status_code=400, detail="session_id e message são obrigatórios.")
    
    try:
        response = agent.handle_message(
            session_id=user_input.session_id,
            user_message=user_input.message
        )
        return {"response": response}
    except Exception as e:
        # Em um app real, faríamos um log mais detalhado do erro
        print(f"Erro ao processar mensagem: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")
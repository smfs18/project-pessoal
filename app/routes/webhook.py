from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from app.services.triage_agent import TriageAgent
import easyocr
import threading

print("Carregando modelo de OCR (EasyOCR)")
reader = easyocr.Reader(['pt'], gpu=False) 
print("Modelo de OCR carregado com sucesso.")


router = APIRouter()
agent = TriageAgent()

class UserInput(BaseModel):
    session_id: str
    message: str

@router.post("/chat", tags=["Chat"])
async def handle_chat_message(user_input: UserInput):
    if not user_input.message or not user_input.session_id:
        raise HTTPException(status_code=400, detail="session_id e message são obrigatórios.")
    
    try:
        response = agent.handle_message(
            session_id=user_input.session_id,
            user_message=user_input.message
        )
        return {"response": response}
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")



@router.post("/ocr-upload", tags=["OCR"])
async def handle_ocr_upload(file: UploadFile = File(...)):
    """
    Recebe um upload de imagem, extrai o texto usando OCR e o retorna.
    """
    try:
        contents = await file.read()
        result = reader.readtext(contents, detail=0, paragraph=True)
        extracted_text = " ".join(result)
        
        print(f"Texto extraído por OCR: {extracted_text}")
        return {"extracted_text": extracted_text}
    except Exception as e:
        print(f"Erro no processamento OCR: {e}")
        raise HTTPException(status_code=500, detail="Não foi possível processar a imagem.")
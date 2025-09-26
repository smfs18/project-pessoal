from app.services.llm_client import llm_client 
from langchain_core.messages import AIMessage 


def test_llm_client_invoke(mocker):
    """
    Testa se nosso cliente chama o método invoke do modelo.
    Usa um mock para evitar uma chamada real à API do Gemini.
    """
    
    resposta_falsa = AIMessage(content="Olá! Sou a ClinicAI. Como posso ajudar?")
    
 
    mocker.patch(
        'langchain_google_genai.chat_models.ChatGoogleGenerativeAI.invoke', 
        return_value=resposta_falsa
    )

    
    mensagens_teste = [{"role": "user", "content": "Oi"}]
    resposta_real = llm_client.invoke(mensagens_teste)

    
    assert resposta_real.content == "Olá! Sou a ClinicAI. Como posso ajudar?"
    assert isinstance(resposta_real, AIMessage)
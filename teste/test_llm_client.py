
from app.services.llm_client import llm_client
from langchain_core.messages import AIMessage

def test_llm_client_invoke(mocker):
    """
    Testa se nosso cliente chama o método invoke do modelo.
    Usa um mock para evitar uma chamada real à API do Gemini.
    """
    # 1. Preparamos uma resposta falsa que o modelo da Gemini deveria retornar
    resposta_falsa = AIMessage(content="Olá! Sou a ClinicAI. Como posso ajudar?")
    
    # 2. Usamos o 'mocker' para substituir o método 'invoke' real do modelo
    #    pela nossa resposta falsa.
    mocker.patch(
        'langchain_google_genai.chat_models.ChatGoogleGenerativeAI.invoke', 
        return_value=resposta_falsa
    )

    # 3. Chamamos o nosso cliente
    mensagens_teste = [{"role": "user", "content": "Oi"}]
    resposta_real = llm_client.invoke(mensagens_teste)

    # 4. Verificamos se a resposta foi a que nós simulamos
    assert resposta_real.content == "Olá! Sou a ClinicAI. Como posso ajudar?"
    assert isinstance(resposta_real, AIMessage)
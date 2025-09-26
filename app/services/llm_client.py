import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()

class LLMClient:
    """
    Uma classe para encapsular a configuração e a instanciação do cliente da LLM.
    Isso centraliza a lógica de conexão com o modelo de linguagem.
    """
    def __init__(self):
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi definida.")
            
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

    def invoke(self, messages):
        """
        Método wrapper para chamar o modelo de linguagem com uma lista de mensagens.
        """
        if not self.model:
            raise ConnectionError("O cliente da LLM não foi inicializado corretamente.")
        return self.model.invoke(messages)


# Criei uma única instância do cliente para ser usada em toda a aplicação.
llm_client = LLMClient()

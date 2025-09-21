from datetime import datetime # Importação do datetime para timestamps
from typing import List, TypedDict, Annotated # Importações de tipagem para melhor clareza e segurança de tipos.
# Importações do LangChain e LangGraph para manipulação de mensagens e construção de grafos de estado.
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END


# Importação o cliente LLM de nosso módulo dedicado.
from app.services.llm_client import llm_client 
# Importação do banco de dados e utilitários de emergência: função para identificar emergências e a resposta padrão.
from app.db.database import get_database
from app.utils.emergency import check_for_emergency, EMERGENCY_RESPONSE

# Definição do estado do agente de triagem usando TypedDict para melhor clareza e tipagem.
class TriageState(TypedDict): #TypedDict é usado para definir a estrutura do estado, é um diciónario sofisticado com tipos fixos.
    messages: Annotated[List[BaseMessage], lambda x, y: x + y] # Define uma lista de mensagens (tanto do usuário quanto do assistente), mas preserva o histórico com a função lambda.
    is_emergency: bool # Indica se a sessão atual foi marcada como emergência, influenciando o fluxo da conversa.

# Criação do prompt do sistema, basicamente, orientamos o comportamento do agente.
SYSTEM_PROMPT = """
**Você é a LIA, uma assistente virtual de triagem para uma clínica de saúde.**

**--- SUA PERSONA E MISSÃO ---**
- Você é acolhedora, empática e profissional. Seu objetivo é guiar o usuário de forma calma, clara e nordestina (sem exageros na linguegem, mantenha o profissionalismo) para coletar informações de triagem.
- Sua missão é coletar de forma estruturada: Queixa Principal, Sintomas, Duração/Frequência, Intensidade, Histórico e Medidas Tomadas. Faça uma pergunta de cada vez.
- Inicie a primeira conversa se apresentando e explicando suas limitações (não sou um médico, não posso dar diagnósticos).

**--- REGRAS CRÍTICAS ---**
- **NÃO FAÇA DIAGNÓSTICOS.**
- **NÃO SUGIRA TRATAMENTOS.**
- **NÃO RESPONDA A PERGUNTAS FORA DO ESCOPO DE SAÚDE.** Se o usuário desviar muito o assunto, gentilmente retorne o foco para a triagem.

**--- PROTOCOLO DE EMERGÊNCIA (IMPORTANTE) ---**
- O sistema possui um verificador de emergência externo. Se a conversa for direcionada para você após um alerta, é porque o alerta era um falso positivo. Nesse caso, ignore a menção de palavras como 'dor no peito' e continue a triagem normalmente, mas com um tom extra de cautela. O sistema já lidou com o alerta principal.
"""
# Criação da classe principal do agente de triagem, em suma especifica o que o agente sabe fazer e como ele deve se comportar.
class TriageAgent:
    def __init__(self): # Construtor da classe, toda vez que a classe for instanciada, este método será chamado.
        self.db = get_database() # Conexão do agente com o banco de dados, permitindo salvar e recuperar sessões.
        
        self.llm_client = llm_client # O agente usa a intância do cliente LLM para interagir com o modelo de linguagem.
        
        self.graph = self._build_graph() # Construção do grafo de estados que define o fluxo da conversa.

    def _build_graph(self): # Define a lógica de funcionamento do agente.
        workflow = StateGraph(TriageState)
        workflow.add_node("emergency_check", self.emergency_check_node)
        workflow.add_node("triage_agent", self.triage_agent_node)
        workflow.set_entry_point("emergency_check")
        workflow.add_conditional_edges(
            "emergency_check",
            self.should_continue_triage,
            {"continue": "triage_agent", "end": END}
        )
        workflow.add_edge("triage_agent", END)
        return workflow.compile()

    def emergency_check_node(self, state: TriageState):
        # (Este método permanece exatamente o mesmo)
        last_message = state['messages'][-1].content
        is_emergency = check_for_emergency(last_message)
        if is_emergency:
            emergency_message = AIMessage(content=EMERGENCY_RESPONSE)
            return {"is_emergency": True, "messages": [emergency_message]}
        return {"is_emergency": False}

    def triage_agent_node(self, state: TriageState):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state['messages']
        
        # Alterado: Usamos nosso cliente para invocar o modelo.
        response = self.llm_client.invoke(messages) 
        
        return {"messages": [response]}

    def should_continue_triage(self, state: TriageState) -> str:
        # (Este método permanece exatamente o mesmo)
        if state['is_emergency']:
            return "end"
        return "continue"

    def handle_message(self, session_id: str, user_message: str) -> str:
        # (Este método permanece exatamente o mesmo)
        session = self.db.find_one({"session_id": session_id})
        if not session:
            initial_state: TriageState = {
                "messages": [HumanMessage(content=user_message)],
                "is_emergency": False
            }
        else:
            messages = [
                HumanMessage(content=msg['content']) if msg['role'] == 'user' 
                else AIMessage(content=msg['content']) 
                for msg in session['messages']
            ]
            initial_state: TriageState = {
                "messages": messages + [HumanMessage(content=user_message)],
                "is_emergency": session.get('is_emergency', False)
            }
        
        if session and session.get('is_emergency', False):
            return EMERGENCY_RESPONSE

        final_state = self.graph.invoke(initial_state)
        self._save_state_to_db(session_id, final_state)
        return final_state['messages'][-1].content

    def _save_state_to_db(self, session_id: str, state: TriageState):
        # (Este método permanece exatamente o mesmo)
        messages_to_save = []
        for msg in state['messages']:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            messages_to_save.append({"role": role, "content": msg.content})
        self.db.update_one(
            {"session_id": session_id},
            {"$set": {"session_id": session_id, "messages": messages_to_save, "is_emergency": state['is_emergency'], "updated_at": datetime.utcnow()}},
            upsert=True
        )
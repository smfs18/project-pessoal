import json 
from datetime import datetime 
from typing import List, TypedDict, Annotated, Optional, Dict, Any 

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from langgraph.graph import StateGraph, END

from app.services.llm_client import llm_client 
from app.db.database import get_database
from app.utils.emergency import check_for_emergency, EMERGENCY_RESPONSE



SYSTEM_PROMPT = """
**Você é a LIA, uma assistente virtual de triagem para uma clínica de saúde.**

**--- SUA PERSONA E MISSÃO ---**
- Você é acolhedora, empática e profissional. Seu objetivo é guiar o usuário de forma calma, clara e com um leve e simpático sotaque nordestino. Mantenha o profissionalismo.
- Sua missão é coletar de forma estruturada: Queixa Principal, Sintomas, Duração/Frequência, Intensidade, Histórico e Medidas Tomadas. Faça uma pergunta de cada vez.
- Inicie a primeira conversa se apresentando e explicando suas limitações (não sou um médico, não posso dar diagnósticos), de forma resumida.
- Quando todas as  informações foram coletadas, finalize a conversa de forma natural e agradeça ao paciente, não se esquecendo de avisar que um profissional de saúde entrará em contato em breve e não precisa repetir as informações.

**--- REGRAS CRÍTICAS E PROTOCOLO DE EMERGÊNCIA ---**
- **NÃO FAÇA DIAGNÓSTICOS.**
- **NÃO SUGIRA TRATAMENTOS.**
- **NÃO RESPONDA A PERGUNTAS FORA DO ESCOPO DE SAÚDE.** Se o usuário desviar muito o assunto, gentilmente retorne o foco para a triagem.

**--- PROTOCOLO DE EMERGÊNCIA ---**
- O sistema possui um verificador de emergência externo. Se a conversa for direcionada para você após um alerta, é porque o alerta era um falso positivo. Nesse caso, ignore a menção de palavras como 'dor no peito' e continue a triagem normalmente, mas com um tom extra de cautela. O sistema já lidou com o alerta principal.
"""

EXTRACTION_PROMPT = """
**Você é um assistente de extração de dados.** Sua única tarefa é analisar a conversa de triagem fornecida e extrair as seguintes informações-chave. Responda APENAS com um objeto JSON válido, sem qualquer texto adicional antes ou depois.

**Campos a Extrair:**
- queixa_principal, sintomas_detalhados, duracao_frequencia, intensidade, historico_relevante, medidas_tomadas

**Instruções Adicionais:**
- Para cada campo, forneça uma string clara e concisa.
- Se a informação para um campo não estiver disponível, retorne `null`.
"""


ROUTER_PROMPT = """
**Você é um roteador de triagem.** Sua função é analisar uma conversa e determinar se a coleta de dados da triagem está completa.
A triagem está completa se os seguintes 6 pontos foram discutidos: Queixa Principal, Sintomas, Duração/Frequência, Intensidade, Histórico e Medidas Tomadas.

Responda APENAS com a palavra "completa" se a triagem terminou, ou "incompleta" se ainda faltam perguntas a serem feitas.

Conversa a ser analisada:
{conversation_history}
"""


class TriageState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    is_emergency: bool
    triage_status: str 
    triage_summary: Optional[Dict[str, Any]]



class TriageAgent:
    def __init__(self):
        self.db = get_database()
        self.llm_client = llm_client
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(TriageState)
        
        workflow.add_node("emergency_check", self.emergency_check_node)
        workflow.add_node("triage_agent", self.triage_agent_node)
        workflow.add_node("triage_router", self.triage_router_node)
        workflow.add_node("summarize_data", self.summarize_data_node)

        workflow.set_entry_point("emergency_check")

        workflow.add_conditional_edges(
            "emergency_check",
            self.should_continue_triage,
            {"continue": "triage_agent", "end": END}
        )
        
        workflow.add_edge("triage_agent", "triage_router")
        
        workflow.add_conditional_edges(
            "triage_router",
            self.should_summarize,
            {
                "continue": END,
                "summarize": "summarize_data"
            }
        )
        
        workflow.add_edge("summarize_data", END)
        return workflow.compile()


    def emergency_check_node(self, state: TriageState):
        last_message = state['messages'][-1].content
        is_emergency = check_for_emergency(last_message)
        if is_emergency:
            emergency_message = AIMessage(content=EMERGENCY_RESPONSE)
            return {"is_emergency": True, "messages": [emergency_message]}
        return {"is_emergency": False}

    def triage_agent_node(self, state: TriageState):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state['messages']
        response = self.llm_client.invoke(messages) 
        return {"messages": [response]}
        
    def triage_router_node(self, state: TriageState):
        """Novo nó que decide se a triagem está completa."""
        conversation_history = ""
        for msg in state['messages']:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            conversation_history += f"{role}: {msg.content}\n"


        prompt = ROUTER_PROMPT.format(conversation_history=conversation_history)
        response = self.llm_client.invoke([HumanMessage(content=prompt)])
        decision = response.content.strip().lower()
        print(f"Decisão do Roteador: {decision}")
        return {"triage_status": decision}

    def summarize_data_node(self, state: TriageState):
        """Nó que extrai os dados estruturados da conversa."""
        full_conversation = ""
        for msg in state['messages']:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            full_conversation += f"{role}: {msg.content}\n"

            
        extraction_prompt_with_data = f"{EXTRACTION_PROMPT}\n\nConversa a ser analisada:\n{full_conversation}"
        try:
            raw_response = self.llm_client.invoke([HumanMessage(content=extraction_prompt_with_data)])
            cleaned_json_string = raw_response.content.strip().replace("```json", "").replace("```", "")
            summary_data = json.loads(cleaned_json_string)
            print("Dados extraídos com sucesso:", summary_data)
            return {"triage_summary": summary_data}
        except Exception as e:
            print(f"Erro na extração de dados: {e}")
            return {"triage_summary": {"erro": f"Falha na extração: {str(e)}"}}

    def should_continue_triage(self, state: TriageState) -> str:
        if state['is_emergency']:
            return "end"
        return "continue"

    def should_summarize(self, state: TriageState) -> str:
        if state.get("triage_status") == "completa":
            return "summarize"
        return "continue"


    def handle_message(self, session_id: str, user_message: str) -> str:
        session = self.db.find_one({"session_id": session_id})
        
        if session and session.get('is_emergency', False):
            return EMERGENCY_RESPONSE

        messages_from_db = []
        if session and session.get('messages'):
             messages_from_db = [
                HumanMessage(content=msg['content']) if msg['role'] == 'user' 
                else AIMessage(content=msg['content']) 
                for msg in session['messages']
            ]
            
        initial_state: TriageState = {
            "messages": messages_from_db + [HumanMessage(content=user_message)],
            "is_emergency": session.get('is_emergency', False) if session else False,
            "triage_status": "",
            "triage_summary": session.get('triage_summary', None) if session else None
        }
        
        final_state = self.graph.invoke(initial_state)
        self._save_state_to_db(session_id, final_state)
        return final_state['messages'][-1].content

    def _save_state_to_db(self, session_id: str, state: TriageState):
        messages_to_save = []
        for msg in state['messages']:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            messages_to_save.append({"role": role, "content": msg.content, "timestamp": datetime.utcnow()})

        update_fields = {
            "session_id": session_id,
            "messages": messages_to_save,
            "is_emergency": state.get('is_emergency', False),
            "updated_at": datetime.utcnow()
        }
        
        if state.get('triage_summary') is not None:
            update_fields["triage_summary"] = state['triage_summary']

        self.db.update_one(
            {"session_id": session_id},
            {"$set": update_fields},
            upsert=True
        )
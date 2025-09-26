from app.services.llm_client import llm_client
from langchain_core.messages import HumanMessage 


EMERGENCY_DECISION_PROMPT = """
**Você é um assistente de IA treinado para atuar como um classificador de emergência médica em textos curtos.**
Sua única tarefa é analisar o texto do usuário e decidir se ele descreve uma emergência médica que requer atenção imediata.
**Critérios para Emergência (considere SIM):**
- Sintomas cardiovasculares (dor no peito, palpitações fortes).
- Sintomas respiratórios (falta de ar, dificuldade de respirar).
- Sintomas neurológicos súbitos (desmaio, confusão mental, fala arrastada, tontura severa).
- Sangramento intenso e incontrolável.
- Dor descrita como "insuportável", "terrível" ou de intensidade máxima.
- Menção a acidentes graves.
**Critérios para Não Emergência (considere NÃO):**
- Sintomas leves ou moderados (dor de cabeça, tosse, febre baixa).
- Perguntas administrativas (marcar consulta, pedir informações).
- Descrição de sintomas passados que já foram resolvidos.
- Expressões idiomáticas (ex: "morrendo de rir").
**Analise o seguinte texto:**
---
{user_text}
---
**O texto acima descreve uma emergência médica?**
Responda APENAS com a palavra "SIM" se for uma emergência, ou "NÃO" se não for. Não adicione nenhuma outra palavra ou pontuação.
"""

def check_for_emergency(text: str) -> bool:
    """
    Verifica se um texto descreve uma emergência médica usando um LLM como classificador.
    """
    try:
        
        prompt = EMERGENCY_DECISION_PROMPT.format(user_text=text)
        
        
        response = llm_client.invoke([HumanMessage(content=prompt)])
        
        
        decision = response.content.strip().upper()
        
        print(f"🩺 Decisão de Emergência do LLM: '{text[:50]}...' -> {decision}")

        
        return decision == "SIM"

    except Exception as e:
        print(f"❌ Erro ao chamar o LLM para verificação de emergência: {e}")
        return False


EMERGENCY_RESPONSE = (
    "Com base no que você descreveu, seus sintomas podem indicar uma situação de emergência. "
    "Por favor, interrompa nossa conversa e procure o pronto-socorro mais próximo ou "
    "ligue para o SAMU (192) imediatamente. Sua saúde é a prioridade."
)
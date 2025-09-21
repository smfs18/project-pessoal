import re

# Lista de palavras-chave. Pode ser melhorada com o tempo.
EMERGENCY_KEYWORDS = [
    "dor no peito", "falta de ar", "dificuldade para respirar", "desmaio",
    "sangramento intenso", "perda de consciencia", "pressao forte no peito",
    "fala arrastada", "rosto torto", "infarto", "avc", "hemorragia"
]

def check_for_emergency(text: str) -> bool:
    """
    Verifica se o texto contém palavras-chave de emergência.
    """
    text_lower = text.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if re.search(r'\b' + keyword + r'\b', text_lower):
            return True
    return False

EMERGENCY_RESPONSE = (
    "Com base no que você descreveu, seus sintomas podem indicar uma situação de emergência. "
    "Por favor, interrompa nossa conversa e procure o pronto-socorro mais próximo ou "
    "ligue para o SAMU (192) imediatamente. Sua saúde é a prioridade."
)
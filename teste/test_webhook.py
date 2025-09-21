import pytest
import httpx

# O endereço base da nossa API quando ela está rodando localmente
BASE_URL = "http://127.0.0.1:8000"

# Marcamos os testes como assíncronos
@pytest.mark.asyncio
async def test_fluxo_de_conversa_normal():
    """
    Simula uma requisição normal ao endpoint /chat.
    """
    # Usamos um ID de sessão para simular um usuário único
    session_id = "test_user_normal_123"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/chat",
            json={"session_id": session_id, "message": "Olá, estou com febre."}
        )

    # Verificamos se a API respondeu com sucesso
    assert response.status_code == 200
    
    # Verificamos se a resposta tem o formato esperado
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0 # Garante que a resposta não está vazia

@pytest.mark.asyncio
async def test_fluxo_de_emergencia():
    """
    Simula uma requisição de emergência e verifica a resposta específica.
    """
    session_id = "test_user_emergency_456"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/chat",
            json={"session_id": session_id, "message": "Estou com dor no peito!"}
        )

    assert response.status_code == 200
    data = response.json()
    
    # Verificamos se a resposta é a mensagem exata de emergência
    assert "seus sintomas podem indicar uma situação de emergência" in data["response"]
    assert "procure o pronto-socorro mais próximo" in data["response"]
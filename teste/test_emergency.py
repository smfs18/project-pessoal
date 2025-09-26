import pytest 
from app.utils.emergency import check_for_emergency 
from langchain_core.messages import AIMessage 



def test_deve_retornar_true_quando_llm_responde_sim(mocker):
    """
    Testa o caso onde o LLM identifica uma emergência.
    """

    resposta_falsa_do_llm = AIMessage(content="SIM")
    


    mock_invoke = mocker.patch('app.services.llm_client.LLMClient.invoke', return_value=resposta_falsa_do_llm)
    

    texto_de_emergencia = "estou com o peito apertado e meu braço esquerdo formigando"


    resultado = check_for_emergency(texto_de_emergencia)


    assert resultado is True

    mock_invoke.assert_called_once()


def test_deve_retornar_false_quando_llm_responde_nao(mocker):
    """
    Testa o cenário onde o LLM não identifica uma emergência.
    """

    resposta_falsa_do_llm = AIMessage(content="NÃO")
    mocker.patch('app.services.llm_client.LLMClient.invoke', return_value=resposta_falsa_do_llm)
    
    texto_normal = "queria marcar uma consulta para a semana que vem"


    resultado = check_for_emergency(texto_normal)


    assert resultado is False


def test_deve_ser_insensivel_a_caixa_e_espacos_na_resposta(mocker):
    """
    Testa se a nossa lógica de limpeza (strip() e upper()) funciona.
    """

    resposta_falsa_do_llm = AIMessage(content="  sim \n")
    mocker.patch('app.services.llm_client.LLMClient.invoke', return_value=resposta_falsa_do_llm)


    resultado = check_for_emergency("qualquer texto de entrada")


    assert resultado is True


def test_deve_retornar_false_em_caso_de_erro_na_api(mocker):
    """
    Testa o bloco 'try...except' para garantir que a aplicação não quebre se a API falhar.
    """

    mocker.patch('app.services.llm_client.LLMClient.invoke', side_effect=Exception("Erro de conexão com a API"))


    resultado = check_for_emergency("um texto que causará um erro")


    assert resultado is False
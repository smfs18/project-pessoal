import pytest
from app.utils.emergency import check_for_emergency

def test_deve_detectar_emergencia_com_palavra_chave():
    """Garante que a função retorna True para palavras de emergência."""
    texto_emergencia = "Estou com uma forte dor no peito e falta de ar."
    assert check_for_emergency(texto_emergencia) == True

def test_nao_deve_detectar_emergencia_em_texto_normal():
    """Garante que a função retorna False para textos comuns."""
    texto_normal = "Olá, estou com dor de cabeça."
    assert check_for_emergency(texto_normal) == False

def test_deve_ser_sensivel_a_maiusculas_e_minusculas():
    """Garante que a detecção não diferencia maiúsculas/minúsculas."""
    texto_emergencia = "SOCORRO DESMAIO"
    assert check_for_emergency(texto_emergencia) == True
# supabase/utils.py
"""Funções para integração com a API REST do Supabase (GET, POST, etc)."""

import requests
from supabase.config import montar_credenciais
from supabase.headers import montar_headers

# Nome da tabela no Supabase
TABELA = "ponto_eletronico"

def registrar_ponto(login: str, senha: str, payload: dict) -> bool:
    """
    Envia os dados de ponto para a tabela no Supabase.

    Args:
        login (str): Nome do empregado.
        senha (str): Fragmento usado para montar a URL.
        payload (dict): Dados a serem enviados (data, horas, etc).

    Returns:
        bool: True se sucesso, False se erro.
    """
    pass


def obter_ponto_do_dia(login: str, senha: str, data: str) -> dict:
    """
    Busca o ponto do dia específico para um empregado.

    Args:
        login (str): Nome do empregado.
        senha (str): Fragmento para montar a URL.
        data (str): Data no formato YYYY-MM-DD.

    Returns:
        dict: Dados encontrados, ou {} se não houver.
    """
    pass


def consultar_pontos_do_mes(login: str, senha: str, empregado: str, mes: str) -> list:
    """
    Busca todos os pontos de um empregado em um determinado mês.

    Args:
        login (str): Quem está acessando (admin ou empregado).
        senha (str): Fragmento da URL.
        empregado (str): Nome da empregada.
        mes (str): Mês no formato '2025-07'.

    Returns:
        list: Lista de registros encontrados.
    """
    pass

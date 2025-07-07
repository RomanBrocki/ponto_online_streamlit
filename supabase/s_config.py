"""Montagem das credenciais completas de acesso ao Supabase com base na senha digitada."""
from interface import i_vars
from supabase.s_secrets import URL_INICIO, URL_FIM, KEY_FIXA

def montar_credenciais(senha: str) -> tuple[str, str]:
    """
    Recebe a senha digitada pelo usuário e monta a URL e a KEY de acesso ao Supabase.

    Args:
        senha (str): Fragmento da URL digitado como senha.

    Returns:
        tuple: (url_completa, key_fixa)
    """
    url = f"{URL_INICIO}{senha}{URL_FIM}"
    key = KEY_FIXA
    return url, key

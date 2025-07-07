"""Geração de headers padrão para requisições à API REST do Supabase."""

from typing import Dict

def montar_headers(api_key: str) -> dict:
    """
    Monta os headers necessários para autenticação e requisição à API REST do Supabase.

    Args:
        api_key (str): Chave de acesso (geralmente KEY_FIXA).

    Returns:
        dict: Headers padrão com Authorization e Content-Type.
    """
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

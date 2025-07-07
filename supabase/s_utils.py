import requests
from typing import Dict, List, Any, Optional


def obter_registros(url: str, headers: Dict[str, str], params: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """
    Obtém registros do Supabase via requisição GET.

    Args:
        url (str): URL da tabela no Supabase.
        headers (Dict[str, str]): Headers com autenticação.
        params (Optional[Dict[str, str]]): Filtros opcionais (ex: {'usuario': 'rani'}).

    Returns:
        List[Dict[str, Any]]: Lista de registros ou lista vazia se não houver dados ou erro.
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


def inserir_registro(url: str, headers: Dict[str, str], dados: Dict[str, Any]) -> bool:
    """
    Insere um novo registro no Supabase via requisição POST.

    Args:
        url (str): URL da tabela no Supabase.
        headers (Dict[str, str]): Headers com autenticação.
        dados (Dict[str, Any]): Dados a serem inseridos.

    Returns:
        bool: True se a inserção for bem-sucedida, False caso contrário.
    """
    try:
        response = requests.post(url, headers=headers, json=dados)
        return response.status_code == 201
    except Exception:
        return False


def deletar_registro(url: str, headers: Dict[str, str], id_registro: int) -> bool:
    """
    Deleta um registro do Supabase via requisição DELETE.

    Args:
        url (str): URL da tabela no Supabase.
        headers (Dict[str, str]): Headers com autenticação.
        id_registro (int): ID do registro a ser deletado.

    Returns:
        bool: True se a exclusão for bem-sucedida, False caso contrário.
    """
    try:
        delete_url = f"{url}?id=eq.{id_registro}"
        response = requests.delete(delete_url, headers=headers)
        return response.status_code == 204
    except Exception:
        return False

def atualizar_registro(url: str, headers: dict, id_registro: int, novos_dados: dict, debug: bool = False) -> bool:
    """
    Atualiza um registro existente no Supabase via requisição PATCH.

    Args:
        url (str): URL da tabela no Supabase.
        headers (dict): Headers com autenticação.
        id_registro (int): ID do registro que será atualizado.
        novos_dados (dict): Campos e valores a serem atualizados.
        debug (bool, opcional): Se True, exibe mensagens de depuração via Streamlit. Padrão é False.

    Returns:
        bool: True se a atualização for bem-sucedida (status 204), False caso contrário.
    """
    try:
        import streamlit as st
        patch_url = f"{url}?id=eq.{id_registro}"

        if debug:
            st.warning(f"[DEBUG] PATCH URL: {patch_url}")
            st.warning(f"[DEBUG] DADOS: {novos_dados}")

        response = requests.patch(patch_url, headers=headers, json=novos_dados)

        if response.status_code != 204:
            if debug:
                st.error(f"[DEBUG] STATUS: {response.status_code}")
                try:
                    st.error(f"[DEBUG] ERRO JSON: {response.json()}")
                except Exception:
                    st.error(f"[DEBUG] ERRO TEXTO: {response.text}")
        return response.status_code == 204

    except Exception as e:
        if debug:
            st.error(f"[DEBUG] EXCEÇÃO: {e}")
        return False


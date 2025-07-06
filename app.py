# app.py
"""Interface principal do aplicativo de ponto eletrônico."""

import streamlit as st
from supabase.config import montar_credenciais
from interface.vars import LOGINS_VALIDOS

st.set_page_config(page_title="Ponto Eletrônico", layout="centered")

def main():
    st.title("📋 Ponto Eletrônico da Casa")

    # Campos de login e senha
    login = st.text_input("Nome de acesso").strip().lower()
    senha = st.text_input("Senha de acesso", type="password").strip().lower()

    # Validação básica
    if not login or not senha:
        st.warning("Informe seu nome e senha.")
        return

    if login not in LOGINS_VALIDOS:
        st.error("Login inválido.")
        return

    try:
        url, key = montar_credenciais(senha)
    except Exception as e:
        st.error("Erro ao montar credenciais de acesso.")
        return

    # Salva na sessão
    st.session_state.perfil = LOGINS_VALIDOS[login]
    st.session_state.login = login
    st.session_state.url = url
    st.session_state.key = key

    # Roteia para a interface correta
    if st.session_state.perfil == "empregada":
        interface_empregada()
    elif st.session_state.perfil == "admin":
        interface_admin()

def interface_empregada():
    """Interface de marcação de ponto para a empregada."""
    pass

def interface_admin():
    """Interface de visualização e relatórios para o administrador."""
    pass

if __name__ == "__main__":
    main()

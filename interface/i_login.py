import streamlit as st
from interface.i_vars import LOGINS_VALIDOS, CARGA_HORARIA_PADRAO
from supabase.s_config import montar_credenciais
from supabase.s_headers import montar_headers

# === Tela de Login ===
def exibir_tela_login() -> bool:
    """
    Exibe a interface de login do aplicativo.

    - Solicita login e senha do usuário.
    - Verifica se o login é válido e monta as credenciais com base na senha fornecida.
    - Se a autenticação for bem-sucedida, armazena os dados na sessão e recarrega a página.

    Returns:
        bool: True se o login for bem-sucedido, False caso contrário.
    """
    with st.form("login_form"):
        login = st.text_input("Login", placeholder="Digite seu login (ex: rani)").lower()
        senha = st.text_input("Senha", placeholder="Digite sua senha", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            if login in LOGINS_VALIDOS:
                try:
                    url, key = montar_credenciais(senha)
                    headers = montar_headers(key)

                    st.session_state["autenticado"] = True
                    st.session_state["login"] = login
                    st.session_state["perfil"] = LOGINS_VALIDOS[login]
                    st.session_state["url"] = url
                    st.session_state["headers"] = headers
                    st.rerun()

                except Exception:
                    st.error("Erro ao montar credenciais. Verifique a senha.")
            else:
                st.error("Login inválido.")
    return False
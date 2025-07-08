import streamlit as st
from interface.i_vars import LOGINS_VALIDOS, CARGA_HORARIA_PADRAO
from interface.i_visuais import exibir_cabecalho, exibir_mensagem_boas_vindas, aplicar_estilo_background
from interface.i_login import exibir_tela_login
from interface.i_empregada import exibir_interface_empregada
from interface.i_admin import exibir_interface_admin
from interface.i_helpers import obter_data_formatada

from datetime import datetime


# === Main ===

def main():
    """
    Função principal do aplicativo Streamlit.

    - Configura o layout e o título da página.
    - Exibe a tela de login caso o usuário não esteja autenticado.
    - Após login bem-sucedido, exibe o cabeçalho, mensagem de boas-vindas e a data atual.
    - Redireciona para a interface da empregada ou do administrador, conforme o perfil.
    - Exibe botão de logout para encerrar a sessão.
    """
    st.set_page_config(page_title="Ponto Online", layout="centered")
    aplicar_estilo_background()

    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        exibir_tela_login()
        return

    # Após login bem-sucedido
    exibir_cabecalho()
    perfil = st.session_state["perfil"]
    exibir_mensagem_boas_vindas(perfil)
    data_iso = obter_data_formatada()
    data_legivel = datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    st.markdown(f"📅 Hoje é {data_legivel}")
    st.markdown("---")

    if perfil == "empregada":
        exibir_interface_empregada()
    elif perfil == "admin":
        exibir_interface_admin()

    st.markdown("---")
    if st.button("🚪 Sair"):
        st.session_state.clear()
        st.rerun()


if __name__ == "__main__":
    main()

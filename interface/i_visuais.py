import streamlit as st

"""Funções de estilo e layout visual do app (background, cabeçalho, etc)."""

import streamlit as st
import base64

def aplicar_estilo_background():
    """
    Aplica uma imagem de fundo ao app, ocupando toda a tela.
    A imagem 'assets/bg.png' é convertida para base64 e embutida no CSS.
    """
    image_path = "assets/bg.png"
    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Imagem de fundo 'assets/bg.png' não encontrada.")


def exibir_cabecalho():
    """
    Aplica o fundo e exibe um título moderno e centralizado no topo do app.
    """
    aplicar_estilo_background()
    st.markdown(
        """
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 3rem;
            padding-bottom: 2rem;
        ">
            <h1 style="
                color: #ffffff;
                font-size: 2.8rem;
                font-weight: 600;
                text-shadow: 0 2px 6px rgba(0,0,0,0.3);
                margin: 0;
            ">
                🕒 Ponto Online
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )


def exibir_mensagem_boas_vindas(perfil: str) -> None:
    """Exibe uma mensagem de boas-vindas personalizada conforme o perfil do usuário."""
    if perfil == "empregada":
        mensagem = "Bem-vinda! Marque seus horários com facilidade e tranquilidade."
    elif perfil == "admin":
        mensagem = "Bem-vindo! Aqui você pode consultar registros, gerar relatórios e acompanhar a jornada."
    else:
        mensagem = "Bem-vindo ao sistema de ponto online."

    st.markdown(
        f"""
        <div style="
            background-color: rgba(255, 255, 255, 0.15);
            padding: 1rem 2rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 1.2rem;
            margin-top: 1rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        ">
            {mensagem}
        </div>
        """,
        unsafe_allow_html=True,
    )


# interface/i_admin.py

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from interface.i_vars import LOGINS_VALIDOS
from supabase.s_utils import obter_registros, atualizar_registro, inserir_registro, deletar_registro
from relatorio.r_pdf_generator import gerar_pdf_relatorio
from calendar import monthrange


def exibir_interface_admin():
    """
    Exibe a interface administrativa do app.

    - Permite selecionar um mês e consultar os registros da empregada.
    - Exibe os registros do mês atual com opção de gerar PDF.
    - Permite ativar o modo de edição e escolher um dia específico para editar ou excluir marcações.
    """
    st.subheader("Painel Administrativo")

    empregado = list(LOGINS_VALIDOS.keys())[0]  # único por enquanto
    url_base = st.session_state["url"] + "/rest/v1/ponto_eletronico"
    headers = st.session_state["headers"]

    col1, col2 = st.columns(2)
    with col1:
        ano = st.selectbox("Ano", [2024, 2025], index=1)
    with col2:
        mes = st.selectbox("Mês", list(range(1, 13)), format_func=lambda m: f"{m:02d}")

    # Ajuste para buscar datas em formato ISO: '2025-06'
    mes_str = f"{ano}-{mes:02d}"
    mes_inicio = f"{mes_str}-01"
    ultimo_dia = monthrange(ano, mes)[1]
    mes_fim = f"{mes_str}-{ultimo_dia:02d}"

    # Monta a URL completa com os filtros de data
    url_filtrada = f"{url_base}?empregado=eq.{empregado}&data=gte.{mes_inicio}&data=lte.{mes_fim}"
    registros = obter_registros(url_filtrada, headers)


    df = pd.DataFrame(registros)

    st.markdown("---")
    st.markdown("### Ações")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Gerar PDF"):
            nome_arquivo = f"relatorio_{empregado}_{mes_str}.pdf"
            pdf_bytes = gerar_pdf_relatorio({"registros": registros}, nome_arquivo)
            if pdf_bytes:
                st.session_state["pdf_bytes"] = pdf_bytes
                st.session_state["nome_arquivo_pdf"] = nome_arquivo
            else:
                st.error("Erro ao gerar o PDF.")

        if "pdf_bytes" in st.session_state:
            st.download_button(
                label="📥 Baixar PDF",
                data=st.session_state["pdf_bytes"],
                file_name=st.session_state["nome_arquivo_pdf"],
                mime="application/pdf",
                key="botao_download_pdf"
            )


    with col2:
        if st.button("✏️ Editar Registros"):
            st.session_state["modo_edicao"] = True

    if st.session_state.get("modo_edicao"):
        st.markdown("---")
        st.markdown("### 🗓 Escolha o dia para editar")
        data_escolhida = st.date_input("Data", format="DD/MM/YYYY")
        if data_escolhida:
            exibir_editor_data(data_escolhida, empregado, url_base, headers)


def normalizar_horario(valor: str) -> str:
    """
    Converte uma entrada de horário incompleta (como '8', '800', '830') para o formato 'HH:MM'.

    Args:
        valor (str): Entrada do usuário, potencialmente mal formatada.

    Returns:
        str: Horário formatado como 'HH:MM'. Retorna string vazia se o valor não for válido.
    """
    valor = valor.strip().replace(":", "")
    if not valor.isdigit():
        return ""
    if len(valor) <= 2:
        return f"{int(valor):02d}:00"
    elif len(valor) == 3:
        h, m = int(valor[0]), int(valor[1:])
    elif len(valor) == 4:
        h, m = int(valor[:2]), int(valor[2:])
    else:
        return ""
    h = max(0, min(h, 23))
    m = max(0, min(m, 59))
    return f"{h:02d}:{m:02d}"


def exibir_editor_data(data: date, empregado: str, url: str, headers: dict):
    """
    Exibe o formulário para editar ou inserir registros de ponto de um dia específico.

    Args:
        data (date): Data a ser consultada ou editada.
        empregado (str): Nome do empregado (usuário) vinculado ao registro.
        url (str): URL base da tabela no Supabase.
        headers (dict): Headers de autenticação para a API REST do Supabase.
    
    - Permite editar horários de entrada, saída, retorno e saída final.
    - Inclui campo de observação (ex: feriado, falta, etc).
    - Permite salvar alterações ou excluir o registro do dia.
    """
    data_str = data.isoformat()
    filtros = {"empregado": f"eq.{empregado}", "data": f"eq.{data_str}"}
    registros = obter_registros(url, headers, filtros)
    registro = registros[0] if registros else None

    st.markdown(f"#### Registro do dia {data.strftime('%d/%m/%Y')}")
    campos = ["entrada", "saida_almoco", "volta_almoco", "saida_final"]
    valores = {}

    col1, col2 = st.columns(2)
    for i, campo in enumerate(campos):
        with (col1 if i < 2 else col2):
            label = {
                "entrada": "🟢 Entrada",
                "saida_almoco": "🍽️ Saída para almoço",
                "volta_almoco": "🔄 Retorno do almoço",
                "saida_final": "🔴 Saída final"
            }.get(campo, campo)

            valor_inicial = registro[campo] if registro and campo in registro else ""
            valores[campo] = st.text_input(label, valor_inicial, key=f"{campo}_{data_str}")

    # Campo de observação
    opcoes_obs = ["", "Feriado", "Dispensa Justificada", "Falta"]
    valor_obs = registro["observacao"] if registro and "observacao" in registro else ""
    valores["observacao"] = st.selectbox("📌 Observação", options=opcoes_obs, index=opcoes_obs.index(valor_obs) if valor_obs in opcoes_obs else 0, key=f"obs_{data_str}")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("💾 Salvar", key=f"salvar_{data_str}"):
            valores = {
                k: normalizar_horario(v) if k != "observacao" else v
                for k, v in valores.items()
                if k == "observacao" or normalizar_horario(v)
            }

            sucesso = False
            if registro:
                sucesso = atualizar_registro(url, headers, registro["id"], valores)
            else:
                novo = {
                    "empregado": empregado,
                    "data": data.isoformat(),
                    **valores
                }
                sucesso = inserir_registro(url, headers, novo)

            if sucesso:
                st.success("Registro salvo com sucesso.")
                st.rerun()
            else:
                st.error("Erro ao salvar o registro.")

    if registro:
        with col4:
            if st.button("🗑 Excluir", key=f"excluir_{data_str}"):
                if deletar_registro(url, headers, registro["id"]):
                    st.success("Registro excluído.")
                    st.rerun()
                else:
                    st.error("Erro ao excluir registro.")





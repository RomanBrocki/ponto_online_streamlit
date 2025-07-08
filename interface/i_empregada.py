import streamlit as st
from interface.i_vars import CARGA_HORARIA_PADRAO
from interface.i_helpers import obter_data_formatada, obter_hora_formatada
from supabase.s_utils import obter_registros, inserir_registro, atualizar_registro
from relatorio.r_utils import analisar_jornada

from datetime import datetime, timedelta


# === Interface da Empregada ===
def exibir_interface_empregada():
    """
    Exibe a interface de marcação de ponto para a empregada.

    - Mostra o saldo de horas extras ou déficit no mês atual.
    - Sugere o próximo horário a ser registrado com base na jornada de trabalho.
    - Permite o registro de entrada, saída para almoço, retorno do almoço e saída final.
    - Informa quando a jornada está completa.
    """
    st.subheader("Marcar ponto do dia")
    data_hoje = obter_data_formatada()
    hora_agora = obter_hora_formatada()
    empregado = st.session_state["login"]
    url_base = st.session_state["url"] + "/rest/v1/ponto_eletronico"
    headers = st.session_state["headers"]

    # === Cálculo do balanço de horas extras ===
    mes_atual = datetime.now().strftime("%m")
    ano_atual = datetime.now().strftime("%Y")

    # Busca todos os registros do empregado
    filtros_mes = {"empregado": f"eq.{empregado}"}
    registros_mes = obter_registros(url_base, headers, filtros_mes)

    # Filtra manualmente para o mês atual
    registros_mes_atual = [
        r for r in registros_mes
        if datetime.strptime(r["data"], "%Y-%m-%d").month == int(mes_atual)
        and datetime.strptime(r["data"], "%Y-%m-%d").year == int(ano_atual)
    ]


    resultado = analisar_jornada(registros_mes_atual, mes_atual, ano_atual)

    # Cálculo de horas esperadas com base na jornada padrão
    dias_trabalhados = sum(1 for d in resultado["por_dia"] if d["tipo"] in ["normal", "falta"])
    horas_esperadas = dias_trabalhados * CARGA_HORARIA_PADRAO
    saldo_min = int(round((resultado["total_horas"] - horas_esperadas) * 60))
    sinal = "+" if saldo_min > 0 else "-" if saldo_min < 0 else ""
    h, m = divmod(abs(saldo_min), 60)
    saldo_str = f"{sinal}{h}:{m:02d}"

    # Exibição do resumo
    if saldo_min >= 0:
        st.success(f"📈 Horas extras acumuladas no mês: **{saldo_str}**")
    else:
        st.warning(f"📉 Saldo negativo no mês: **{saldo_str}**")


    # Busca registro do dia
    filtros = {"empregado": f"eq.{empregado}", "data": f"eq.{data_hoje}"}
    registros = obter_registros(url_base, headers, filtros)
    registro = registros[0] if registros else None
    # Sugestão de horário à marcar
    if registro and registro.get("entrada"):
        try:
            def normalizar(horario_str):
                """
                Normaliza um horário string para o formato 'HH:MM', removendo segundos ou pontos.

                Args:
                    horario_str (str): Texto contendo o horário.

                Returns:
                    str: Horário no formato 'HH:MM'.
                """
                return ":".join(horario_str.strip().split(".")[0].split(":")[:2])

            entrada = normalizar(registro["entrada"])
            entrada_dt = datetime.strptime(f"{data_hoje} {entrada}", "%Y-%m-%d %H:%M")

            saida_almoco_dt = volta_almoco_dt = None
            if registro.get("saida_almoco"):
                saida_almoco = normalizar(registro["saida_almoco"])
                saida_almoco_dt = datetime.strptime(f"{data_hoje} {saida_almoco}", "%Y-%m-%d %H:%M")

            if registro.get("volta_almoco"):
                volta_almoco = normalizar(registro["volta_almoco"])
                volta_almoco_dt = datetime.strptime(f"{data_hoje} {volta_almoco}", "%Y-%m-%d %H:%M")

            if saida_almoco_dt and not volta_almoco_dt:
                retorno_sugerido = saida_almoco_dt + timedelta(hours=1)
                st.info(f"🕐 **Retorno sugerido do almoço:** {retorno_sugerido.strftime('%H:%M')}")
            elif volta_almoco_dt:
                intervalo_almoco = volta_almoco_dt - saida_almoco_dt if saida_almoco_dt else timedelta()
                saida_sugerida = entrada_dt + timedelta(hours=CARGA_HORARIA_PADRAO) + intervalo_almoco
                st.info(f"💡 **Saída sugerida (ajustada):** {saida_sugerida.strftime('%H:%M')}")
            else:
                saida_sugerida = entrada_dt + timedelta(hours=CARGA_HORARIA_PADRAO)
                st.info(f"💡 **Saída sugerida:** {saida_sugerida.strftime('%H:%M')}")
        except Exception as e:
            st.warning(f"Erro ao calcular sugestão: {e}")




    # Identifica o próximo campo a ser preenchido
    ordem_campos = [
        ("entrada", "🟢 Entrada"),
        ("saida_almoco", "🍽️ Saída para almoço"),
        ("volta_almoco", "🔄 Retorno do almoço"),
        ("saida_final", "🔴 Saída final"),
    ]
    proximo_campo = None
    for campo, label in ordem_campos:
        if not registro or registro.get(campo) is None:
            proximo_campo = (campo, label)
            break

    def registrar(campo: str, label: str):
        """
        Registra o horário atual no campo correspondente para o dia atual.

        Args:
        campo (str): Nome do campo no banco (ex: "entrada", "saida_almoco").
        label (str): Rótulo para exibição na mensagem de sucesso.
        """
        if registro:
            id_registro = registro["id"]
            sucesso = atualizar_registro(url_base, headers, id_registro, {campo: hora_agora})
        else:
            novo = {
                "empregado": empregado,
                "data": data_hoje,
                campo: hora_agora
            }
            sucesso = inserir_registro(url_base, headers, novo)

        if sucesso:
            st.success(f"{label} registrada às {hora_agora}!")
            st.rerun()
        else:
            st.error("Erro ao registrar o ponto.")

    # Exibe botão apenas se houver campo disponível
    if proximo_campo:
        campo, label = proximo_campo
        if st.button(label):
            registrar(campo, label)
    else:
        st.success("✅ Jornada de trabalho completa!")
        st.caption("Todos os pontos do dia já foram marcados.")
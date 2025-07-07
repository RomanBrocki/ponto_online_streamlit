from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from typing import Optional
from relatorio.r_utils import analisar_jornada


def gerar_pdf_relatorio(dados: dict, nome_arquivo: str) -> Optional[bytes]:
    """
    Gera um relatório mensal em PDF com base nos registros de ponto fornecidos.

    - Analisa os dados usando `analisar_jornada()`.
    - Cria uma tabela com os horários registrados por dia.
    - Exibe observações e saldos diários.
    - Inclui um resumo com número de faltas, feriados, dispensas justificadas e total de horas extras.

    Args:
        dados (dict): Dicionário com a chave "registros" contendo a lista de registros de ponto.
        nome_arquivo (str): Nome sugerido para o arquivo PDF (usado apenas no botão de download).

    Returns:
        Optional[bytes]: Conteúdo do PDF em bytes, pronto para ser salvo ou baixado.
                         Retorna None se não houver registros válidos.
    """
    registros = dados.get("registros", [])
    if not registros:
        return None

    # Extrai empregado e mês/ano
    empregado = registros[0].get("empregado", "empregado")
    data_exemplo = registros[0].get("data")
    data_dt = datetime.strptime(data_exemplo, "%Y-%m-%d")
    mes = f"{data_dt.month:02d}"
    ano = f"{data_dt.year}"

    resumo = analisar_jornada(registros, mes, ano)
    dias = resumo["por_dia"]

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=30, bottomMargin=30)
    estilos = getSampleStyleSheet()
    elementos = []

    # Título
    titulo = f"Relatório de Ponto - {empregado.capitalize()} - {mes}/{ano}"
    elementos.append(Paragraph(titulo, estilos["Title"]))
    elementos.append(Spacer(1, 12))

    # Cabeçalho da tabela
    dados_tabela = [[
        "Data", "Entrada", "Saída Almoço", "Retorno Almoço", "Saída Final", "Observação", "Balanço"
    ]]

    total_horas_extras = 0.0
    contagem = {"falta": 0, "feriado": 0, "dispensa justificada": 0}

    for dia in dias:
        data_str = dia["data"]
        tipo = dia["tipo"]
        horas = dia["horas_trabalhadas"]

        # Pega o registro da data (se houver)
        registro = next((r for r in registros if r.get("data") == datetime.strptime(data_str, "%d/%m/%Y").date().isoformat()), None)

        if tipo == "normal" and registro:
            entrada = (registro.get("entrada") or "")[:5]
            saida_almoco = (registro.get("saida_almoco") or "")[:5]
            volta_almoco = (registro.get("volta_almoco") or "")[:5]
            saida_final = (registro.get("saida_final") or "")[:5]
            obs = registro.get("observacao") or "—"
            saldo = int(round((horas - 8) * 60))
            sinal = "+" if saldo > 0 else "-" if saldo < 0 else ""
            abs_min = abs(saldo)
            h, m = divmod(abs_min, 60)
            saldo_str = f"{sinal}{h}:{m:02d}"

            total_horas_extras += saldo
        elif tipo in ["falta", "justificada"]:
            entrada = saida_almoco = volta_almoco = saida_final = "—"
            obs = (registro.get("observacao") if registro else "").capitalize()
            saldo_str = "0h" if tipo == "justificada" else "-8h"
            if obs.lower() in contagem:
                contagem[obs.lower()] += 1
        else:
            entrada = saida_almoco = volta_almoco = saida_final = "—"
            obs = "—" if tipo != "pendente" else "Pendente"
            saldo_str = "—"

        dados_tabela.append([
            data_str, entrada, saida_almoco, volta_almoco, saida_final, obs, saldo_str
        ])

    # Monta tabela
    tabela = Table(dados_tabela, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 12))

    # Resumo
    elementos.append(Paragraph("Resumo do Mês", estilos["Heading3"]))
    elementos.append(Paragraph(f"- Faltas: {contagem['falta']}", estilos["Normal"]))
    elementos.append(Paragraph(f"- Feriados: {contagem['feriado']}", estilos["Normal"]))
    elementos.append(Paragraph(f"- Dispensas Justificadas: {contagem['dispensa justificada']}", estilos["Normal"]))
    sinal_total = "+" if total_horas_extras > 0 else "-" if total_horas_extras < 0 else ""
    h_total, m_total = divmod(abs(int(total_horas_extras)), 60)
    elementos.append(Paragraph(f"- Horas Extras no Mês: {sinal_total}{h_total}:{m_total:02d}", estilos["Normal"]))


    doc.build(elementos)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


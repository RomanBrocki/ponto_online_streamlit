from datetime import datetime, timedelta
from datetime import date
from typing import List, Dict

from datetime import datetime, timedelta, date
from typing import List, Dict

def analisar_jornada(dados: List[Dict], mes: str, ano: str) -> Dict:
    """
    Analisa os registros de ponto de um determinado mês e ano.

    - Agrupa os registros por dia útil.
    - Classifica cada dia como: 'normal', 'justificada', 'falta' ou 'pendente'.
    - Calcula o total de horas trabalhadas e faltas.
    - Identifica pendências (dias úteis sem marcações completas).
    - Considera feriados e dispensas justificadas a partir do campo 'observacao'.

    Args:
        dados (List[Dict]): Lista de registros brutos do Supabase.
        mes (str): Mês no formato 'MM'.
        ano (str): Ano no formato 'AAAA'.

    Returns:
        Dict: Resultado da análise contendo:
            - "total_horas": soma das horas válidas (float)
            - "faltas": número de dias classificados como falta (int)
            - "pendencias": lista de datas com registros incompletos (List[str])
            - "por_dia": lista com dados analisados por dia (List[Dict])
    """
    hoje = datetime.now().date()
    total_horas = 0.0
    faltas = 0
    pendencias = []
    por_dia = []
    acumulado = 0.0

    registros_por_data = {r['data']: r for r in dados}

    data_inicio = datetime.strptime(f"01/{mes}/{ano}", "%d/%m/%Y").date()
    prox_mes = data_inicio.replace(day=28) + timedelta(days=4)
    data_fim = prox_mes - timedelta(days=prox_mes.day)

    dia_atual = data_inicio
    while dia_atual <= min(data_fim, hoje):
        if dia_atual.weekday() >= 5:
            dia_atual += timedelta(days=1)
            continue

        data_str = dia_atual.isoformat()
        registro = registros_por_data.get(data_str)

        tipo = "pendente"
        horas_trabalhadas = 0.0

        if not registro:
            pendencias.append(dia_atual.strftime("%d/%m/%Y"))
        else:
            obs_raw = registro.get("observacao")
            obs = obs_raw.strip().lower() if isinstance(obs_raw, str) else ""

            if obs in ["feriado", "dispensa justificada"]:
                tipo = "justificada"
            elif obs == "falta":
                tipo = "falta"
                horas_trabalhadas = -8.0
                total_horas += horas_trabalhadas
                faltas += 1
            elif all(registro.get(k) for k in ["entrada", "saida_almoco", "volta_almoco", "saida_final"]):
                try:
                    h_entrada = datetime.strptime(registro["entrada"], "%H:%M:%S")
                    h_saida_almoco = datetime.strptime(registro["saida_almoco"], "%H:%M:%S")
                    h_volta_almoco = datetime.strptime(registro["volta_almoco"], "%H:%M:%S")
                    h_saida_final = datetime.strptime(registro["saida_final"], "%H:%M:%S")

                    tempo_total = (h_saida_final - h_entrada) - (h_volta_almoco - h_saida_almoco)
                    horas_trabalhadas = round(tempo_total.total_seconds() / 3600, 2)
                    tipo = "normal"
                    total_horas += horas_trabalhadas
                except Exception:
                    tipo = "pendente"
                    pendencias.append(dia_atual.strftime("%d/%m/%Y"))
            else:
                pendencias.append(dia_atual.strftime("%d/%m/%Y"))

        acumulado += horas_trabalhadas
        por_dia.append({
            "data": dia_atual.strftime("%d/%m/%Y"),
            "tipo": tipo,
            "horas_trabalhadas": horas_trabalhadas,
            "acumulado": round(acumulado, 2)
        })

        dia_atual += timedelta(days=1)

    return {
        "total_horas": round(total_horas, 2),
        "faltas": faltas,
        "pendencias": pendencias,
        "por_dia": por_dia
    }



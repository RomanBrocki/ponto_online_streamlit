# relatorio/utils.py
"""Funções de apoio para cálculo de horas trabalhadas, faltas, extras etc."""

def calcular_horas_trabalhadas(entrada, saida, almoco_ida, almoco_volta):
    """
    Calcula o total de horas líquidas trabalhadas no dia.

    Args:
        entrada (str)
        saida (str)
        almoco_ida (str)
        almoco_volta (str)

    Returns:
        float: Total de horas trabalhadas no dia.
    """
    pass

def identificar_faltas(dias_mes, dias_com_ponto):
    """
    Compara dias do mês com dias que possuem ponto para detectar faltas.

    Args:
        dias_mes (list[str])
        dias_com_ponto (list[str])

    Returns:
        list[str]: Datas faltantes.
    """
    pass

def somar_extras_e_saldo(dias_completos, carga_horaria_padrao):
    """
    Soma saldo de horas extras a partir de dias com ponto completo.

    Args:
        dias_completos (list[dict])
        carga_horaria_padrao (int)

    Returns:
        float: Total de horas extras.
    """
    pass

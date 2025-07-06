# interface/helpers.py
"""Funções auxiliares da interface: formatação, validação, sugestões."""

def formatar_hora(hora_str: str) -> str:
    """
    Formata uma hora no formato HH:MM para exibição.

    Args:
        hora_str (str): Hora como string.

    Returns:
        str: Hora formatada.
    """
    pass

def sugerir_hora_saida(hora_entrada: str, carga_horaria: int) -> str:
    """
    Sugere o horário final com base na entrada e jornada.

    Args:
        hora_entrada (str): Ex: '08:30'
        carga_horaria (int): Jornada do dia (ex: 8)

    Returns:
        str: Hora sugerida de saída.
    """
    pass

def validar_campos_ponto(dados: dict) -> bool:
    """
    Verifica se os campos necessários do ponto estão preenchidos.

    Args:
        dados (dict): Campos do dia.

    Returns:
        bool: True se válido, False se incompleto.
    """
    pass

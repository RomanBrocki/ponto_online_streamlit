from datetime import datetime
import pytz

fuso_brasil = pytz.timezone("America/Sao_Paulo")

def obter_data_formatada() -> str:
    """
    Retorna a data atual formatada no padrão brasileiro (dd/mm/aaaa).

    Returns:
        str: Data atual no formato 'dd/mm/aaaa'.
    """
    return datetime.now(fuso_brasil).strftime("%Y-%m-%d")


def obter_hora_formatada() -> str:
    """
    Retorna a hora atual formatada no padrão brasileiro (HH:MM).

    Returns:
        str: Hora atual no formato 'HH:MM'.
    """
    return datetime.now(fuso_brasil).strftime("%H:%M:%S")


def validar_campo_preenchido(valor: str) -> bool:
    """
    Verifica se o campo fornecido está preenchido (não é vazio, nulo ou só espaços).

    Args:
        valor (str): Texto a ser validado.

    Returns:
        bool: True se o valor estiver preenchido, False caso contrário.
    """
    return bool(valor and valor.strip())


# interface/vars.py
"""Variáveis globais e configurações do app de ponto."""

# Carga horária diária padrão (em horas)
CARGA_HORARIA_PADRAO = 8

# Logins válidos: login → perfil
LOGINS_VALIDOS = {
    "rani": "empregada",
    "brocki": "admin"
}

# Lista de nomes de empregadas (útil para dropdowns ou relatórios)
EMPREGADAS = ["rani"]

# Nome da tabela usada no Supabase (reforça visibilidade fora de supabase/utils.py)
NOME_TABELA = "ponto_eletronico"

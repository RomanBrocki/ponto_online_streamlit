"""Variáveis globais e configurações do app de ponto."""

# Configuração geral
CARGA_HORARIA_PADRAO = 8  # horas por dia

# Usuárias com perfil de empregada (para dropdowns e relatórios)
EMPREGADAS = ["rani"]

# Mapeamento de logins para perfis de acesso
LOGINS_VALIDOS = {
    "rani": "empregada",
    "brocki": "admin"
}

# Nome da tabela principal no Supabase
NOME_TABELA = "ponto_eletronico"
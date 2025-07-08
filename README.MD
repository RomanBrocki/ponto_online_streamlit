# 🕒 Ponto Online Residencial

Um aplicativo simples de ponto eletrônico para uso residencial, feito com [Streamlit](https://streamlit.io/) e [Supabase](https://supabase.com/). O objetivo é permitir que uma empregada doméstica registre seus horários de forma segura e que os administradores acompanhem as jornadas e gerem relatórios mensais.

---

## 🌟 Funcionalidades

### Para a empregada

* Registro de ponto do **dia atual**:

  * 🟢 Entrada
  * 🍽️ Saída para almoço
  * 🔄 Retorno do almoço
  * 🔴 Saída final
* Sugestão automática de:

  * Horário de retorno do almoço (após 1h)
  * Horário de saída final (ajustado pela carga horária e intervalo real de almoço)
* Exibição do saldo mensal de horas (positivas ou negativas)
* Bloqueio automático após jornada completa
* Visualização das marcações feitas no dia

### Para o administrador

* Consulta de registros por mês e por empregada
* Edição e exclusão de qualquer marcação
* Inclusão de observações como:

  * Feriado
  * Falta
  * Dispensa Justificada
* Geração de relatórios mensais em PDF com:

  * Tabela de marcações por dia
  * Saldos diários
  * Resumo de horas extras, faltas e feriados

### Lógicas internas importantes

* Cada empregada pode ter **apenas um registro por data** (evita duplicidade)
* A jornada de trabalho é considerada **completa** quando os quatro campos estão preenchidos
* O saldo mensal considera:

  * Dias úteis
  * Horas efetivamente registradas
  * Observações de justificativa ou falta

---

## 🔐 Login e Segurança

### Mecanismo

* O login é feito com:

  * **Login**: identifica o perfil (ex: `rani`, `brocki`)
  * **Senha**: fragmento exclusivo que completa a URL de acesso
* Isso monta dinamicamente:

  * `URL = URL_INICIO + senha + URL_FIM`
  * `KEY = chave opcional gerada com base na senha`

### Benefícios

* Nenhuma credencial sensível é armazenada diretamente no repositório
* O projeto pode ser público sem comprometer segurança

---

## 🗃️ Estrutura da Base de Dados (Supabase)

A aplicação utiliza uma tabela única chamada `ponto_eletronico` hospedada no Supabase. Ela armazena todas as marcações de ponto realizadas pelos usuários com os seguintes campos:

| Campo         | Tipo | Descrição                                                            |
| ------------- | ---- | -------------------------------------------------------------------- |
| id            | int  | Chave primária, gerada automaticamente                               |
| empregado     | text | Nome do empregado (ex: "rani")                                       |
| data          | date | Data do ponto (no formato ISO, ex: 2025-07-08)                       |
| entrada       | text | Horário de entrada (ex: "08:00:00")                                  |
| saida\_almoco | text | Horário de saída para o almoço                                       |
| volta\_almoco | text | Horário de retorno do almoço                                         |
| saida\_final  | text | Horário de saída final do expediente                                 |
| observacao    | text | Comentário opcional: "feriado", "falta", "dispensa justificada" etc. |

### Regras e Garantias

* 🔒 A combinação `empregado + data` deve ser única — isso é garantido pela lógica da aplicação
* 🧠 O sistema só permite um registro por dia por empregado, seja criado pela própria empregada ou pelo administrador
* ⏱️ Os horários são registrados sequencialmente e exibidos após preenchidos
* 🗓️ O saldo mensal é calculado com base na jornada esperada (`CARGA_HORARIA_PADRAO`) e nas marcações efetivas do mês

---

## 📅 Estrutura do Projeto

```bash
ponto_online/
├── app.py                        # Arquivo principal do Streamlit
│
├── interface/                   # Interface do usuário
│   ├── i_vars.py                  # Variáveis globais (logins, carga horária)
│   ├── i_visuais.py               # Estilos visuais (CSS, cabeçalho)
│   ├── i_login.py                 # Tela de login
│   ├── i_empregada.py             # Tela da empregada (marcação do dia atual)
│   ├── i_admin.py                 # Tela administrativa (consulta, edição, PDF)
│   └── i_helpers.py               # Funções auxiliares de data, hora, validação
│
├── supabase/                    # Integração com Supabase
│   ├── s_secrets.py               # Fragmentos da URL/KEY
│   ├── s_config.py                # Montagem de URL/KEY
│   ├── s_headers.py               # Headers padrão de acesso
│   └── s_utils.py                 # Funções de leitura, inserção, atualização e exclusão
│
├── relatorio/                   # Lógicas de análise e geração de PDF
│   ├── r_utils.py                 # Cálculo de saldo mensal e análise por dia
│   └── r_pdf_generator.py         # Geração de relatório mensal em PDF
│
├── assets/                      # Imagens e estilos visuais (ex: fundo do app)
├── requirements.txt             # Lista de dependências
└── README.md                    # Este documento
```

---

## 🚀 Instalação e Execução

```bash
# Clone o repositório
git clone https://github.com/RomanBrocki/ponto_online_streamlit
cd ponto_online

# Crie e ative a venv
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app.py
```

---

## ✍️ Autor

* Roman Wladyslaw Brocki Neto

Este projeto foi desenvolvido com o apoio do ChatGPT, utilizado para geração de ideias, revisão de código e documentação técnica.

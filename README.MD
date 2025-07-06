# 🕒 Ponto Eletrônico Residencial

Este projeto é um aplicativo de ponto eletrônico simples, feito com [Streamlit](https://streamlit.io/) e [Supabase](https://supabase.com/), para registrar e consultar jornadas de trabalho de empregadas domésticas.

## 🎯 Funcionalidades

- Marcação de ponto do dia atual:
  - Entrada
  - Saída para almoço
  - Retorno do almoço
  - Saída final
- Sugestão automática de horário de saída com base na jornada diária
- Controle de acesso por login (empregada ou administrador)
- Consulta de registros por período (interface administrativa)
- Geração de relatórios mensais em PDF com resumo de faltas e horas extras

---

## 🔐 Login e Segurança

O acesso ao app é feito com **dois campos**:

- **Login**: identifica o perfil (`rani` ou `brocki`, por exemplo)
- **Senha**: um fragmento exclusivo que completa a URL de acesso ao Supabase

### ✳️ Como funciona a segurança:

- O código **não expõe diretamente** a URL nem a API Key do banco
- No login, a senha digitada é usada para **compor dinamicamente**:
  - A URL de acesso (`URL_INICIO + senha + URL_FIM`)
  - A KEY, se desejado
- Isso permite manter o repositório público sem expor credenciais sensíveis

### 🔁 Lógica de acesso (fork por perfil):

- Se o login for de uma **empregada**, o app:
  - Exibe apenas o formulário de ponto do **dia atual**
  - Salva os dados no Supabase com o nome da empregada

- Se o login for do **administrador**, o app:
  - Exibe um painel de seleção por empregada e mês
  - Permite gerar **relatórios em PDF**
  - Exibe totais de faltas e horas extras

---

## 🧱 Estrutura do Projeto

```bash
ponto_online/
├── app.py                        # Interface principal com Streamlit
│
├── interface/                   # Elementos da interface e variáveis globais
│   ├── vars.py                  # Logins, carga horária, nomes
│   ├── visuais.py               # Estilo visual e layout
│   └── helpers.py               # Funções auxiliares para a interface
│
├── supabase/                    # Integração com a API REST do Supabase
│   ├── secrets.py               # Fragmentos públicos da URL e Key
│   ├── config.py                # Montagem dinâmica de URL/KEY
│   ├── headers.py               # Headers padrão
│   └── utils.py                 # Leitura, escrita e consulta no Supabase
│
├── relatorio/                   # Cálculo e geração de PDFs
│   ├── utils.py                 # Regras de negócio (faltas, horas)
│   └── pdf_generator.py         # Geração de relatórios em PDF
│
├── assets/                      # Imagens e estilos adicionais
│
├── requirements.txt             # Dependências do projeto
└── README.md                    # Este documento
⚙️ Instalação e Execução
bash
Copiar
Editar
# Clone o repositório
git clone https://github.com/seu-usuario/ponto_online.git
cd ponto_online

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app.py

✍️ Autor
Roman Wladyslaw Brocki Neto
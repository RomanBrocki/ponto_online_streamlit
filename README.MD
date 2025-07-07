# 🕒 Ponto Online para Empregadas Domésticas

Este é um aplicativo de ponto eletrônico simples, desenvolvido em **Python com Streamlit**, voltado ao **registro e acompanhamento da jornada de trabalho de empregadas domésticas**. Ele permite registrar horários, calcular automaticamente o saldo de horas extras ou déficit, e gerar relatórios mensais em PDF para controle.

---

## 📌 Objetivo

Facilitar o controle de jornada de empregadas domésticas de forma simples, acessível e segura — diretamente pelo navegador, com acesso por login e senha, sem necessidade de infraestrutura complexa.

---

## ⚙️ Funcionalidades

### 👤 **Perfil Empregada**
- Marcação de ponto em quatro etapas:
  - 🟢 Entrada
  - 🍽️ Saída para almoço
  - 🔄 Retorno do almoço
  - 🔴 Saída final
- Sugestão automática do próximo horário com base:
  - No tempo decorrido desde o início da jornada
  - No tempo de almoço já computado
- Exibição do **saldo mensal de horas extras ou horas faltantes**
- Preenchimento automático da data e hora atual
- Interface simplificada, voltada para uso no celular

---

### 🛠️ **Perfil Administrador**
- Seleção de mês e ano para consulta
- Visualização completa dos registros de uma empregada
- Edição detalhada dos registros de um dia específico:
  - Inserção e modificação de horários
  - Marcação de faltas, feriados ou dispensas justificadas
  - Exclusão de registros
- Geração de **relatório mensal em PDF**, com:
  - Tabela de registros diários
  - Observações e saldos por dia
  - Resumo de faltas, feriados e horas extras no mês

---

## 🔐 Login e Segurança

O sistema usa **login e senha**, com duas funções importantes:

- **Login** identifica o perfil (`empregada` ou `admin`)
- **Senha** é usada como fragmento secreto para compor a URL de acesso ao Supabase

### Como funciona:
- A URL e a chave de API **não ficam visíveis no código**
- Durante o login, a senha digitada **completa dinamicamente a URL**
  - Exemplo: `https://crvqo<senha>.supabase.co`
- Isso permite manter o repositório público sem risco de vazamento de credenciais

---

## 🧱 Estrutura do Projeto

```bash
ponto_online/
├── app.py                        # Arquivo principal com controle da navegação
│
├── interface/                   # Interface e elementos visuais
│   ├── i_vars.py                 # Carga horária e logins válidos
│   ├── i_visuais.py              # Layout visual (background, título, boas-vindas)
│   ├── i_login.py                # Tela de login e montagem de sessão
│   ├── i_empregada.py            # Interface para marcação de ponto
│   ├── i_admin.py                # Interface para visualização e edição dos registros
│   └── i_helpers.py              # Funções auxiliares de data e validação
│
├── supabase/                    # Integração com o banco Supabase
│   ├── s_secrets.py              # Fragmentos da URL e chave pública
│   ├── s_config.py               # Monta URL e KEY com base na senha digitada
│   ├── s_headers.py              # Headers padrão para requisições REST
│   └── s_utils.py                # Funções para CRUD no Supabase (GET, POST, PATCH, DELETE)
│
├── relatorio/                   # Lógica de análise e geração de PDFs
│   ├── r_utils.py                # Análise da jornada (faltas, extras, pendências)
│   └── r_pdf_generator.py        # Geração do relatório em PDF
│
├── assets/                      # Imagens e estilos adicionais (ex: fundo da página)
│
├── requirements.txt             # Dependências do projeto
└── README.md                    # Este documento
```

---

## 📦 Requisitos

O projeto usa bibliotecas populares do ecossistema Python:

```txt
streamlit
requests
reportlab
pandas
numpy
python-dateutil
matplotlib
```

Você pode copiá-las para seu próprio `requirements.txt`.

---

## 🚀 Instalação e Execução

```bash
# Clone o repositório
git clone https://github.com/RomanBrocki/ponto_online_streamlit
cd ponto_online

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app.py
```

---

## 📊 Observações Técnicas

- O projeto assume uma tabela no Supabase chamada `ponto_eletronico`, com os campos:
  - `id`, `empregado`, `data`, `entrada`, `saida_almoco`, `volta_almoco`, `saida_final`, `observacao`
- Todos os horários são armazenados como `HH:MM:SS`
- A autenticação é feita via chave pública (`anon key`) segura apenas para leitura/escrita controlada — sem permissões administrativas
- Os dados são manipulados exclusivamente via **API REST**, sem SDK

---

## ✍️ Autor

Roman Wladyslaw Brocki Neto  
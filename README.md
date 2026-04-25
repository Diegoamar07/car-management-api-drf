# 🚗 Car Management API (Django REST)

Este repositório contém o núcleo da lógica de uma API de gerenciamento de veículos desenvolvida com **Django REST Framework**.

## 🧠 Lógica e Funcionalidades
- **CRUD Completo:** Gerenciamento de veículos através de `ModelViewSets`.
- **Cálculo de Desconto Automático:** O `CarSerializer` inclui um campo calculado (`discounted_value`) que aplica 10% de desconto sobre o valor original do veículo.
- **Roteamento Organizado:** Separação clara entre as rotas de API (`/api/`) e as páginas da aplicação.

## 📂 Arquivos de Lógica Incluídos
- `models.py`: Definição do modelo Car (essencial para o banco de dados).
- `serializers.py`: Transformação de dados e lógica de campos calculados.
- `views.py`: Controladores REST que gerenciam o ciclo de vida das requisições.
- `urls.py`: (Main) Configuração global e inclusão do prefixo /api/.
- `api_urls.py`: Definição dos endpoints da API.

## 🛠️ Tecnologias
- **Python 3.x**
- **Django** & **Django REST Framework**
- **SQLite/PostgreSQL** (Banco de dados)

## 🚀 Como Executar a API
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Realize as migrações do banco:
   ```bash
   python manage.py migrate
   ```
3. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```
4. Acesse os endpoints da API em: `http://localhost:8000/api/`

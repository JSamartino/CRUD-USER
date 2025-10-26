# CRUD de Usuários - API REST Flask

API REST completa para gerenciamento de usuários com operações de criação, leitura, atualização e exclusão (CRUD). Desenvolvido com Flask e SQLAlchemy.

## 📋 Sobre o Projeto

Esta API permite gerenciar usuários com campos de nome, email e telefone. Oferece validações robustas, tratamento de erros e operações de soft delete (desabilitação em vez de exclusão física).

## 🛠 Tecnologias Utilizadas

- **Python 3.9+**
- **Flask 3.1.2** - Framework web
- **Flask-SQLAlchemy 3.1.1** - ORM para banco de dados
- **Flask-Migrate 4.1.0** - Migrações de banco de dados
- **SQLite** - Banco de dados (desenvolvimento)
- **Pytest 8.4.2** - Framework de testes
- **SQLAlchemy 2.0.44** - Ferramentas de banco de dados

## 📁 Estrutura do Projeto

```
CRUS USER/
├── app/
│   ├── __init__.py              # Inicialização da aplicação Flask
│   ├── controllers/
│   │   └── user_controller.py   # Lógica de negócio e rotas da API
│   └── models/
│       └── user.py              # Modelo de dados User
├── tests/
│   ├── conftest.py              # Configuração dos testes
│   ├── test_user_api.py         # Testes da API
│   └── test_user_model.py       # Testes do modelo
├── instance/                     # Banco de dados SQLite (gerado automaticamente)
├── config.py                    # Configurações da aplicação
├── run.py                       # Arquivo principal para executar a aplicação
├── requirements.txt             # Dependências do projeto
└── README.md                    # Este arquivo
```

## ⚙️ Pré-requisitos

Antes de começar, você precisa ter instalado:
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. **Clone o repositório** (se aplicável):
```bash
git clone <url-do-repositorio>
cd "CRUD-USER"
```

2. **Crie um ambiente virtual**:
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**:

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

## ▶️ Como Executar

1. **Certifique-se de que o ambiente virtual está ativado**

2. **Execute a aplicação**:
```bash
python run.py
```

3. **A API estará disponível em**:
   - `http://127.0.0.1:5000`
   - `http://localhost:5000`

## 🧪 Executando os Testes

Para executar todos os testes:

```bash
pytest
```

Para executar com mais detalhes:

```bash
pytest -v
```

Para executar testes específicos:

```bash
# Apenas testes do modelo
pytest tests/test_user_model.py

# Apenas testes da API
pytest tests/test_user_api.py
```

**Cobertura de testes**: O projeto possui 21 testes automatizados (7 do modelo, 14 da API).

## 📚 Documentação da API

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Listar Todos os Usuários
**GET** `/api/users`

Retorna todos os usuários habilitados.

**Resposta de Sucesso (200):**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "João Silva",
            "email": "joao@example.com",
            "phone": "11999999999",
            "enabled": true,
            "created_at": "2025-10-26T17:00:00",
            "updated_at": "2025-10-26T17:00:00"
        }
    ],
    "count": 1
}
```

#### 2. Buscar Usuário por Telefone
**GET** `/api/users/{phone}`

**Parâmetros:**
- `phone` (string): Telefone do usuário

**Resposta de Sucesso (200):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "João Silva",
        "email": "joao@example.com",
        "phone": "11999999999",
        "enabled": true,
        "created_at": "2025-10-26T17:00:00",
        "updated_at": "2025-10-26T17:00:00"
    }
}
```

**Resposta de Erro (404):**
```json
{
    "success": false,
    "message": "Usuário com telefone {phone} não encontrado."
}
```

#### 3. Criar Usuário
**POST** `/api/users`

**Body (JSON):**
```json
{
    "name": "Maria Santos",
    "email": "maria@example.com",
    "phone": "11988888888"
}
```

**Campos:**
- `name` (string, obrigatório): Nome do usuário
- `email` (string, obrigatório): Email do usuário
- `phone` (string, opcional): Telefone do usuário
- `enabled` (boolean, opcional): Status do usuário (padrão: true)

**Resposta de Sucesso (201):**
```json
{
    "success": true,
    "message": "Usuário criado com sucesso",
    "data": {
        "id": 1,
        "name": "Maria Santos",
        "email": "maria@example.com",
        "phone": "11988888888",
        "enabled": true,
        "created_at": "2025-10-26T17:00:00",
        "updated_at": "2025-10-26T17:00:00"
    }
}
```

**Resposta de Erro (400):**
```json
{
    "success": false,
    "message": "Campo name é obrigatório"
}
```

**Resposta de Erro (409):**
```json
{
    "success": false,
    "message": "Email já está em uso"
}
```

#### 4. Atualizar Usuário
**PUT** `/api/users/{phone}`

**Parâmetros:**
- `phone` (string): Telefone do usuário

**Body (JSON):**
```json
{
    "name": "João Santos",
    "email": "joao.novo@example.com"
}
```

**Campos Atualizáveis:**
- `name` (string, opcional): Novo nome
- `email` (string, opcional): Novo email

**Resposta de Sucesso (200):**
```json
{
    "success": true,
    "message": "Usuário atualizado com sucesso",
    "data": {
        "id": 1,
        "name": "João Santos",
        "email": "joao.novo@example.com",
        "phone": "11999999999",
        "enabled": true,
        "created_at": "2025-10-26T17:00:00",
        "updated_at": "2025-10-26T17:30:00"
    }
}
```

**Resposta de Erro (404):**
```json
{
    "success": false,
    "message": "Usuário com telefone {phone} não encontrado"
}
```

**Resposta de Erro (409):**
```json
{
    "success": false,
    "message": "E-mail já cadastrado"
}
```

#### 5. Desabilitar Usuário (Soft Delete)
**DELETE** `/api/users/{phone}`

**Parâmetros:**
- `phone` (string): Telefone do usuário

**Resposta de Sucesso (200):**
```json
{
    "success": true,
    "message": "Usuário removido com sucesso"
}
```

**Nota**: Este endpoint não exclui o usuário fisicamente do banco de dados. Ele apenas define `enabled` como `false`. Usuários desabilitados não aparecem na listagem.

## 🔒 Validações Implementadas

### Nome
- Mínimo de 2 caracteres
- Máximo de 100 caracteres
- Apenas letras, acentos, espaços, hífens e apostrofes permitidos

### Email
- Formato de email válido
- Obrigatório
- Deve ser único no sistema
- Convertido para minúsculas automaticamente

### Telefone
- Apenas números permitidos
- Mínimo de 10 dígitos
- Opcional
- Deve ser único no sistema

## 🗄️ Estrutura do Banco de Dados

### Tabela `users`

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| id | Integer | Primary Key | Identificador único |
| name | String(100) | NOT NULL | Nome do usuário |
| email | String(120) | NOT NULL, UNIQUE | Email do usuário |
| phone | String(20) | UNIQUE | Telefone do usuário |
| enabled | Boolean | Default: True | Status do usuário |
| created_at | DateTime | Auto | Data de criação |
| updated_at | DateTime | Auto | Data da última atualização |

## 🐛 Tratamento de Erros

A API retorna códigos de status HTTP apropriados:

- **200**: Sucesso
- **201**: Criado com sucesso
- **400**: Requisição inválida (dados incorretos)
- **404**: Recurso não encontrado
- **409**: Conflito (email/telefone já cadastrado)
- **500**: Erro interno do servidor

## 🔍 Códigos de Status HTTP Utilizados

- `200 OK`: Operação bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Dados inválidos ou faltando
- `404 Not Found`: Recurso não encontrado
- `409 Conflict`: Email ou telefone já cadastrado
- `500 Internal Server Error`: Erro no servidor

## 📝 Exemplos de Uso com cURL

### Criar usuário:
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "phone": "11999999999"
  }'
```

### Buscar todos os usuários:
```bash
curl -X GET http://localhost:5000/api/users
```

### Buscar usuário por telefone:
```bash
curl -X GET http://localhost:5000/api/users/11999999999
```

### Atualizar usuário:
```bash
curl -X PUT http://localhost:5000/api/users/11999999999 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Santos",
    "email": "joao.santos@example.com"
  }'
```

### Desabilitar usuário:
```bash
curl -X DELETE http://localhost:5000/api/users/11999999999
```


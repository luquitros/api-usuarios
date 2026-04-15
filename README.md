# Users API

API de usuarios com Django REST Framework e autenticacao JWT.

Este projeto fornece uma base para cadastro, autenticacao e gerenciamento de perfis com diferentes tipos de usuario, como `aluno`, `professor` e `admin`.

## Funcionalidades

- Cadastro de usuarios com criacao automatica de perfil
- Login com JWT
- Refresh de token
- Endpoint `me/` para consultar e editar o proprio perfil
- Controle de acesso por tipo de usuario
- Swagger UI para documentacao interativa
- Estrutura pronta para Django Admin
- Testes basicos da API

## Tecnologias

- Python
- Django
- Django REST Framework
- Simple JWT
- drf-spectacular

## Estrutura

```text
.
|-- admin.py
|-- apps.py
|-- models.py
|-- permissions.py
|-- serializers.py
|-- settings.py
|-- tests.py
|-- urls.py
|-- views.py
|-- README.md
```

## Modelos

### `Profile`

Perfil vinculado ao `User` padrao do Django.

Campos principais:

- `user_type`: `aluno`, `professor` ou `admin`
- `phone`
- `birth_date`
- `bio`
- `avatar_url`

## Endpoints

Base sugerida: `/`

### Autenticacao

- `POST /login/` -> gera `access` e `refresh`
- `POST /refresh/` -> renova o token de acesso

### Documentacao

- `GET /schema/` -> schema OpenAPI
- `GET /docs/` -> Swagger UI

### Usuarios

- `POST /users/` -> cria um novo usuario
- `GET /users/` -> lista usuarios, apenas para `admin`
- `GET /users/{id}/` -> detalhe do usuario
- `PATCH /users/{id}/` -> atualiza usuario
- `DELETE /users/{id}/` -> remove usuario, apenas para `admin`
- `GET /users/me/` -> retorna o usuario autenticado
- `PATCH /users/me/` -> atualiza o proprio perfil

## Exemplo de cadastro

```json
{
  "username": "teacher",
  "password": "Teacher123!",
  "email": "teacher@example.com",
  "first_name": "Ada",
  "last_name": "Lovelace",
  "profile": {
    "user_type": "professor",
    "phone": "11999999999",
    "birth_date": "1990-10-15",
    "bio": "Docente de matematica.",
    "avatar_url": "https://example.com/avatar.png"
  }
}
```

## Exemplo de login

### Requisicao

```json
{
  "username": "teacher",
  "password": "Teacher123!"
}
```

### Resposta

```json
{
  "refresh": "seu-refresh-token",
  "access": "seu-access-token"
}
```

## Como rodar localmente

### 1. Criar e ativar ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Criar migracoes

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Criar superusuario

```bash
python manage.py createsuperuser
```

### 5. Rodar o servidor

```bash
python manage.py runserver
```

## Configuracao JWT

O projeto usa `JWTAuthentication` como autenticacao padrao no DRF.

Se quiser acessar rotas protegidas, envie o token no header:

```text
Authorization: Bearer seu-access-token
```

## Permissoes

- Usuarios nao autenticados podem se cadastrar
- Usuarios comuns podem visualizar e editar apenas os proprios dados
- Usuarios `admin` podem listar e gerenciar todos os usuarios
- Apenas administradores podem criar ou promover usuarios com `user_type = admin`

## Testes

Para executar os testes:

```bash
python manage.py test
```

## Proximos passos

- Adicionar documentacao Swagger/OpenAPI
- Implementar logout com blacklist de tokens
- Adicionar filtros e busca
- Criar endpoints para dominio escolar, como turmas, disciplinas e matriculas

## Autor

Projeto pronto para evoluir como base de autenticacao e gerenciamento de usuarios em APIs Django.

# Users API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-REST-green)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

API de usuarios com Django REST Framework e autenticacao JWT.

Este projeto fornece uma base para cadastro, autenticacao e gerenciamento de perfis com diferentes tipos de usuario, como `aluno`, `professor` e `admin`.

## Funcionalidades

- Cadastro de usuarios com criacao automatica de perfil
- Login com JWT
- Refresh de token
- Logout com blacklist de refresh token
- Endpoint `me/` para consultar e editar o proprio perfil
- Controle de acesso por tipo de usuario
- Paginacao, busca, filtros e ordenacao no endpoint de usuarios
- Throttle para login e requisicoes gerais
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
|-- manage.py
|-- config/
|   |-- urls.py
|   |-- asgi.py
|   |-- wsgi.py
|   `-- settings/
|       |-- base.py
|       |-- dev.py
|       `-- prod.py
|-- users/
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- permissions.py
|   |-- serializers.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   `-- tests/
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
- `POST /logout/` -> invalida `refresh` token (blacklist)
- `POST /refresh/` -> renova o token de acesso

### Documentacao

- `GET /schema/` -> schema OpenAPI
- `GET /docs/` -> Swagger UI

### Usuarios

- `POST /users/` -> cria um novo usuario
- `GET /users/` -> lista usuarios, apenas para `admin`
- `GET /users/?profile__user_type=aluno` -> filtra por tipo de perfil
- `GET /users/?search=student` -> busca por username/email/nome
- `GET /users/?ordering=username` -> ordena resultados
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

### 3. Configurar variaveis de ambiente

Use o arquivo de exemplo como base:

```bash
copy .env.example .env
```

### 4. Criar migracoes

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar superusuario

```bash
python manage.py createsuperuser
```

### 6. Rodar o servidor

```bash
python manage.py runserver
```

Por padrao o projeto usa `config.settings.dev`.

Para rodar com outro ambiente:

```bash
$env:DJANGO_SETTINGS_MODULE="config.settings.prod"
python manage.py runserver
```

## Configuracao JWT

O projeto usa `JWTAuthentication` como autenticacao padrao no DRF.

Se quiser acessar rotas protegidas, envie o token no header:

```text
Authorization: Bearer seu-access-token
```

Para fazer logout (blacklist), envie o `refresh` token:

```json
{
  "refresh": "seu-refresh-token"
}
```

## Seguranca e configuracao

- `prod.py` exige `DJANGO_SECRET_KEY` e `DJANGO_ALLOWED_HOSTS`
- HTTPS forcado em producao com `SECURE_SSL_REDIRECT`
- Cookies de sessao e CSRF marcados como `secure` em producao
- HSTS habilitado em producao
- Throttle configurado para reduzir abuso de login e flooding
- Tokens JWT com expiracao configuravel, rotacao e blacklist
- Carregamento de `.env` nativo para facilitar setup seguro
- Resposta de erro padronizada para facilitar debug e frontend

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

- Adicionar filtros e busca
- Criar endpoints para dominio escolar, como turmas, disciplinas e matriculas

## Licenca

Este projeto usa a licenca MIT. Veja [LICENSE](LICENSE).

## Autor

Projeto pronto para evoluir como base de autenticacao e gerenciamento de usuarios em APIs Django.

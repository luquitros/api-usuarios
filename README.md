# Users API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-REST-green)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

API de usuarios com Django REST Framework + JWT.

Foco do projeto:
- onboarding rapido para quem vai consumir a API
- autenticacao com fluxo completo (`login` -> `refresh` -> `logout`)
- perfil por tipo de usuario (`aluno`, `professor`, `admin`)
- respostas padronizadas para facilitar frontend/mobile

## Inicio rapido

### 1) Rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 2) Abrir os links principais

- Home da API: `GET /`
- Swagger UI: `GET /docs/`
- OpenAPI schema: `GET /schema/`

### 3) Fluxo minimo de autenticacao

1. `POST /login/` para pegar `access` e `refresh`
2. usar `Authorization: Bearer <access>` nas rotas protegidas
3. `POST /refresh/` quando o `access` expirar
4. `POST /logout/` para invalidar o `refresh`

## Endpoints principais

### Auth

- `POST /login/`
- `POST /refresh/`
- `POST /logout/`

### Users

- `POST /users/` (cadastro publico)
- `GET /users/` (somente admin)
- `GET /users/{id}/`
- `PATCH /users/{id}/`
- `DELETE /users/{id}/` (somente admin)
- `GET /users/me/`
- `PATCH /users/me/`

Filtros no list:
- `?profile__user_type=aluno`
- `?search=student`
- `?ordering=username`

## Contrato de resposta

### Sucesso

```json
{
  "success": true,
  "message": "OK",
  "data": {}
}
```

### Erro

```json
{
  "success": false,
  "message": "Dados invalidos. Revise os campos e tente novamente.",
  "status_code": 400,
  "path": "/users/",
  "errors": {
    "profile": {
      "user_type": [
        "Somente administradores podem criar ou promover usuarios para admin."
      ]
    }
  }
}
```

## Exemplo rapido

### Login request

```json
{
  "username": "teacher",
  "password": "Teacher123!"
}
```

### Login response

```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "refresh": "seu-refresh-token",
    "access": "seu-access-token"
  }
}
```

## Permissoes

- nao autenticado: pode cadastrar usuario
- usuario comum: acessa e edita apenas o proprio registro
- admin: lista e gerencia todos os usuarios
- `superuser` do Django tambem e tratado como admin da API

## Seguranca e config

- JWT com expiracao configuravel, rotacao e blacklist
- throttling para reduzir abuso de login/requisicoes
- CORS por ambiente (`dev` e `prod`)
- `prod.py` exige `DJANGO_SECRET_KEY` e `DJANGO_ALLOWED_HOSTS`
- cookies/headers de seguranca reforcados em producao

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

## Testes

```bash
python manage.py test
```

## Licenca

MIT. Veja `LICENSE`.

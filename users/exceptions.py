from rest_framework.views import exception_handler


def _normalize_errors(data):
    if isinstance(data, dict):
        return {key: _normalize_errors(value) for key, value in data.items()}
    if isinstance(data, (list, tuple)):
        return [_normalize_errors(item) for item in data]
    return str(data)


def _friendly_message(status_code, path):
    if path == '/login/' and status_code in {400, 401}:
        return 'Credenciais invalidas. Verifique usuario e senha.'
    if status_code == 400:
        return 'Dados invalidos. Revise os campos e tente novamente.'
    if status_code == 401:
        return 'Autenticacao necessaria. Faca login para continuar.'
    if status_code == 403:
        return 'Voce nao tem permissao para executar esta acao.'
    if status_code == 404:
        return 'Recurso nao encontrado.'
    if status_code == 429:
        return 'Muitas tentativas em pouco tempo. Tente novamente em instantes.'
    if status_code >= 500:
        return 'Erro interno no servidor. Tente novamente mais tarde.'
    return 'Erro na requisicao.'


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    request = context.get('request')
    path = request.path if request else ''
    normalized_errors = _normalize_errors(response.data)
    message = _friendly_message(response.status_code, path)

    response.data = {
        'success': False,
        'message': message,
        'status_code': response.status_code,
        'path': path,
        'errors': normalized_errors,
    }
    return response

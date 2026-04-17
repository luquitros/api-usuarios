from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    request = context.get('request')
    path = request.path if request else ''

    response.data = {
        'success': False,
        'status_code': response.status_code,
        'path': path,
        'errors': response.data,
    }
    return response

from .base import *  # noqa: F403


DEBUG = False

if SECRET_KEY == 'dev-only-secret-key-change-me':  # noqa: F405
    raise ValueError('DJANGO_SECRET_KEY deve ser definido em producao.')

if not ALLOWED_HOSTS:  # noqa: F405
    raise ValueError('DJANGO_ALLOWED_HOSTS deve ser definido em producao.')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'

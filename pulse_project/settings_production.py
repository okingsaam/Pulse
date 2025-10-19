"""
Configurações específicas para produção
Para usar: python manage.py runserver --settings=pulse_project.settings_production
"""
from .settings import *

# Modo de produção
DEBUG = False

# Hosts permitidos em produção (substitua pelos seus domínios)
ALLOWED_HOSTS = [
    'seu-dominio.com',
    'www.seu-dominio.com',
    'localhost',  # Para testes locais
    '127.0.0.1',  # Para testes locais
]

# Configurações de segurança para HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configurações de cookies
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 hora

# Configurações de cache para produção
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'pulse_prod',
        'TIMEOUT': 300,
    }
}

# Configurações de email para produção
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Substitua pelo seu servidor SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@gmail.com'  # Substitua pelo seu email
EMAIL_HOST_PASSWORD = 'sua-senha-app'  # Use senha de aplicativo
DEFAULT_FROM_EMAIL = 'Sistema Pulse <seu-email@gmail.com>'

# Configurações de logging para produção
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'production.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'error_file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Banco de dados para produção (PostgreSQL recomendado)
# Descomente e configure se usar PostgreSQL
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pulse_db',
        'USER': 'pulse_user',
        'PASSWORD': 'sua_senha_segura',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
"""

# Configurações de arquivos estáticos para produção
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configurações de mídia para produção
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações de sessão
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Middleware adicional para produção
MIDDLEWARE.insert(1, 'django.middleware.security.SecurityMiddleware')

print("⚙️ Configurações de PRODUÇÃO carregadas!")
print("🔒 Modo DEBUG desabilitado")
print("🛡️ Configurações de segurança ativadas")
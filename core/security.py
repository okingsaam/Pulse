"""
SECURITY.PY - Configurações de Segurança para Produção
===================================================
Este arquivo contém configurações importantes de segurança
que devem ser aplicadas quando o sistema for para produção.
"""

import os
from django.core.management.utils import get_random_secret_key

# ==========================================
# CONFIGURAÇÕES DE SEGURANÇA PARA PRODUÇÃO
# ==========================================

def get_security_settings():
    """
    Retorna um dicionário com configurações de segurança
    para serem aplicadas em settings.py
    """
    return {
        # CHAVE SECRETA FORTE
        'SECRET_KEY': get_random_secret_key(),
        
        # DEBUG SEMPRE FALSO EM PRODUÇÃO
        'DEBUG': False,
        
        # HOSTS PERMITIDOS (CONFIGURAR COM SEU DOMÍNIO)
        'ALLOWED_HOSTS': [
            'localhost',
            '127.0.0.1',
            'seu-dominio.com',  # Substitua pelo seu domínio
            'www.seu-dominio.com',
        ],
        
        # CONFIGURAÇÕES HTTPS
        'SECURE_SSL_REDIRECT': True,
        'SECURE_HSTS_SECONDS': 31536000,  # 1 ano
        'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
        'SECURE_HSTS_PRELOAD': True,
        
        # COOKIES SEGUROS
        'SESSION_COOKIE_SECURE': True,
        'CSRF_COOKIE_SECURE': True,
        'SESSION_COOKIE_HTTPONLY': True,
        'CSRF_COOKIE_HTTPONLY': True,
        
        # CONFIGURAÇÕES DE SEGURANÇA ADICAIS
        'SECURE_CONTENT_TYPE_NOSNIFF': True,
        'SECURE_BROWSER_XSS_FILTER': True,
        'X_FRAME_OPTIONS': 'DENY',
        
        # CONFIGURAÇÕES DE SENHA
        'AUTH_PASSWORD_VALIDATORS': [
            {
                'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            },
            {
                'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
                'OPTIONS': {
                    'min_length': 8,
                }
            },
            {
                'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
            },
            {
                'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
            },
        ],
        
        # CONFIGURAÇÕES DE EMAIL (PARA NOTIFICAÇÕES)
        'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'EMAIL_HOST': 'smtp.gmail.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True,
        'EMAIL_HOST_USER': os.getenv('EMAIL_HOST_USER'),
        'EMAIL_HOST_PASSWORD': os.getenv('EMAIL_HOST_PASSWORD'),
        'DEFAULT_FROM_EMAIL': 'Pulse Sistema <noreply@seu-dominio.com>',
        
        # CONFIGURAÇÕES DE LOG
        'LOGGING': {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'file': {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'filename': 'logs/pulse.log',
                },
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                'django': {
                    'handlers': ['file', 'console'],
                    'level': 'INFO',
                    'propagate': True,
                },
                'core': {
                    'handlers': ['file', 'console'],
                    'level': 'INFO',
                    'propagate': True,
                },
            },
        },
    }

# ==========================================
# MIDDLEWARE DE SEGURANÇA PERSONALIZADO
# ==========================================

class SecurityHeadersMiddleware:
    """
    Middleware que adiciona headers de segurança extras
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de segurança adicionais
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response

# ==========================================
# CONFIGURAÇÕES DE BACKUP AUTOMÁTICO
# ==========================================

BACKUP_SETTINGS = {
    'BACKUP_DIR': 'backups/',
    'BACKUP_FREQUENCY': 'daily',  # daily, weekly, monthly
    'KEEP_BACKUPS': 30,  # Manter 30 backups
    'BACKUP_COMPRESS': True,
}
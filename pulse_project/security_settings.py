# ==========================================
# CONFIGURAÇÕES DE SEGURANÇA PARA PRODUÇÃO
# ==========================================

# Configurações de segurança que devem ser habilitadas em produção
# Para habilitar, copie estas configurações para settings.py quando em produção

# Segurança HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Cookies seguros (habilitar apenas com HTTPS)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# HTTPS obrigatório (habilitar apenas com HTTPS)
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Configurações de produção
PRODUCTION_SETTINGS = {
    'DEBUG': False,
    'ALLOWED_HOSTS': ['seu-dominio.com', 'www.seu-dominio.com'],
    'SECRET_KEY': 'GERE_UMA_NOVA_CHAVE_PARA_PRODUCAO',
    'DATABASE_URL': 'postgresql://user:password@localhost:5432/pulse_db'
}

# Middleware de segurança adicional
SECURITY_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Validação de senhas mais rigorosa
AUTH_PASSWORD_VALIDATORS = [
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
]
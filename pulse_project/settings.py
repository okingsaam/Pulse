"""
SETTINGS.PY - Configurações do Sistema Pulse
============================================
Este arquivo contém todas as configurações do Django.
É o "centro de controle" do sistema.
"""

from pathlib import Path

# ==========================================
# CONFIGURAÇÕES BÁSICAS
# ==========================================

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# CHAVE SECRETA (manter em segredo em produção!)
SECRET_KEY = '6SF_t3PDi34vsAETRg0n4VIZdrWq-YyypzluGhSepOIHui5sYKMHaQEfjS1O4rlQUU8'

# MODO DEBUG (True = desenvolvimento, False = produção)
DEBUG = True  # Mantido como True para desenvolvimento local

# Hosts permitidos (em produção, especificar domínios)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver', '*.herokuapp.com']

# Configurações de segurança para produção
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ==========================================
# APLICAÇÕES INSTALADAS
# ==========================================
INSTALLED_APPS = [
    # Interface admin melhorada (deve vir antes do admin padrão)
    'admin_interface',
    'colorfield',
    
    # Apps padrão do Django
    'django.contrib.admin',          # Interface administrativa
    'django.contrib.auth',           # Sistema de autenticação
    'django.contrib.contenttypes',   # Sistema de tipos de conteúdo
    'django.contrib.sessions',       # Gerenciamento de sessões
    'django.contrib.messages',       # Sistema de mensagens
    'django.contrib.staticfiles',    # Arquivos estáticos (CSS, JS, imagens)
    
    # Apps de terceiros
    'rest_framework',        # API REST
    'corsheaders',          # CORS (para frontend separado)
    'crispy_forms',         # Formulários bonitos
    'crispy_bootstrap5',    # Tema Bootstrap 5 para forms
    
    # Nossas aplicações
    'core.apps.CoreConfig', # App principal do sistema
]

# ==========================================
# MIDDLEWARES (camadas de processamento)
# ==========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Segurança
    'django.contrib.sessions.middleware.SessionMiddleware', # Sessões
    'corsheaders.middleware.CorsMiddleware',              # CORS
    'django.middleware.common.CommonMiddleware',          # Funcionalidades comuns
    'django.middleware.csrf.CsrfViewMiddleware',          # Proteção CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autenticação
    'django.contrib.messages.middleware.MessageMiddleware',    # Mensagens
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Anti-clickjacking
]

# URL principal do projeto
ROOT_URLCONF = 'pulse_project.urls'

# ==========================================
# CONFIGURAÇÃO DE TEMPLATES
# ==========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Onde buscar templates
        'APP_DIRS': True,                  # Buscar em apps também
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.admin_stats',  # Estatísticas do admin
            ],
        },
    },
]

# Aplicação WSGI (para deploy)
WSGI_APPLICATION = 'pulse_project.wsgi.application'

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',        # Tipo: SQLite
        'NAME': BASE_DIR / 'db.sqlite3',               # Arquivo do banco
    }
}

# ==========================================
# VALIDAÇÃO DE SENHAS
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==========================================
# CONFIGURAÇÕES REGIONAIS
# ==========================================
LANGUAGE_CODE = 'pt-br'  # Idioma português brasileiro
TIME_ZONE = 'America/Sao_Paulo'  # Fuso horário de São Paulo
USE_I18N = True          # Internacionalização
USE_TZ = True           # Usar timezone

# ==========================================
# ARQUIVOS ESTÁTICOS (CSS, JS, IMAGENS)
# ==========================================
STATIC_URL = 'static/'              # URL para acessar arquivos estáticos
STATICFILES_DIRS = [                # Diretórios de arquivos estáticos
    BASE_DIR / 'static',
]

# ==========================================
# CONFIGURAÇÕES ESPECÍFICAS DO PULSE
# ==========================================

# Campo de chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DJANGO REST FRAMEWORK (API)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # Usar sessões
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',           # Só logados
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20  # 20 items por página
}

# CORS (Cross-Origin Resource Sharing)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React/Vue/Angular local
    "http://127.0.0.1:3000",
    "http://localhost:8000",    # Django local
    "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True    # Permitir cookies

# CRISPY FORMS (formulários bonitos)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# MODELO DE USUÁRIO CUSTOMIZADO
AUTH_USER_MODEL = 'core.User'       # Usar nosso User ao invés do padrão

# CONFIGURAÇÕES DE LOGIN/LOGOUT
LOGIN_URL = '/login/'               # Para onde enviar se não logado
LOGIN_REDIRECT_URL = '/dashboard/'  # Para onde ir após login
LOGOUT_REDIRECT_URL = '/'          # Para onde ir após logout

# ==========================================
# CONFIGURAÇÕES DE CACHE
# ==========================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'pulse-cache',
        'TIMEOUT': 300,  # 5 minutos
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# ==========================================
# CONFIGURAÇÕES DE PERFORMANCE
# ==========================================
# Paginação padrão
DEFAULT_PAGE_SIZE = 10

# Otimizações de banco
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# CONFIGURAÇÕES DE LOGGING
# ==========================================
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
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'pulse.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

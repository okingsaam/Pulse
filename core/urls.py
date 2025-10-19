"""
URLS.PY - Roteamento do Sistema Pulse
=====================================
Este arquivo define qual view será executada para cada URL.
É como um "mapa" que diz: "se o usuário acessar X, execute Y"

ESTRUTURA:
1. Imports necessários
2. Configuração da API REST
3. URLs da aplicação
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .consultorio_views import consultorio_dashboard
from .consultorio_extra_views import consultorio_pacientes, consultorio_agenda, consultorio_financeiro

# ==========================================
# CONFIGURAÇÃO DA API REST
# ==========================================
# O Router cria automaticamente as URLs da API
router = DefaultRouter()
router.register(r'users', views.UserViewSet)              # /api/users/
router.register(r'profissionais', views.ProfissionalViewSet)  # /api/profissionais/
router.register(r'servicos', views.ServicoViewSet)        # /api/servicos/
router.register(r'agendamentos', views.AgendamentoViewSet, basename='agendamento')  # /api/agendamentos/

# ==========================================
# NOME DA APLICAÇÃO (para namespacing)
# ==========================================
app_name = 'core'

# ==========================================
# MAPEAMENTO DE URLs
# ==========================================
urlpatterns = [
    # =====================================
    # URLs PRINCIPAIS DO SITE
    # =====================================
    path('', consultorio_dashboard, name='home'),
    # URL: "/"
    # View: consultorio_dashboard (redirecionado para novo dashboard)
    # Nome: 'core:home' (usado em templates)
    
    path('consultorio/', consultorio_dashboard, name='consultorio_dashboard'),
    # URL: "/consultorio/"
    # View: consultorio_dashboard
    # Função: Dashboard moderno do consultório
    
    path('consultorio/pacientes/', consultorio_pacientes, name='consultorio_pacientes'),
    # URL: "/consultorio/pacientes/"
    
    path('consultorio/agenda/', consultorio_agenda, name='consultorio_agenda'),
    # URL: "/consultorio/agenda/"
    
    path('consultorio/financeiro/', consultorio_financeiro, name='consultorio_financeiro'),
    # URL: "/consultorio/financeiro/"
    
    path('register/', views.register, name='register'),
    # URL: "/register/"
    # View: views.register
    # Função: Cadastro de novos usuários
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # URL: "/login/"
    # View: LoginView do Django (pronta)
    # Template automático: registration/login.html
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # URL: "/logout/"
    # View: LogoutView do Django (pronta)
    # Redireciona para LOGOUT_REDIRECT_URL
    
    path('dashboard/', views.dashboard, name='dashboard'),
    # URL: "/dashboard/"
    # View: views.dashboard
    # Função: Painel principal do usuário
    
    path('agendar/', views.agendar_consulta, name='agendar'),
    # URL: "/agendar/"
    # View: views.agendar_consulta
    # Função: Formulário de agendamento
    
    # =====================================
    # URLs CRUD (apenas para admins)
    # =====================================
    path('profissionais/', views.profissional_list, name='profissional_list'),
    # URL: "/profissionais/"
    # View: views.profissional_list
    # Função: Lista todos os médicos
    
    path('profissionais/novo/', views.profissional_create, name='profissional_create'),
    # URL: "/profissionais/novo/"
    # View: views.profissional_create
    # Função: Cadastrar novo médico
    
    path('servicos/', views.servico_list, name='servico_list'),
    # URL: "/servicos/"
    # View: views.servico_list
    # Função: Lista todos os serviços
    
    path('servicos/novo/', views.servico_create, name='servico_create'),
    # URL: "/servicos/novo/"
    # View: views.servico_create
    # Função: Cadastrar novo serviço
    
    path('agendamentos/', views.agendamento_list, name='agendamento_list'),
    # URL: "/agendamentos/"
    # View: views.agendamento_list
    # Função: Lista agendamentos (filtrado por usuário)
    
    # =====================================
    # URLs DE RELATÓRIOS E AGENDA
    # =====================================
    path('agenda/', include('core.reports_urls')),
    # URLs para relatórios e agenda visual
    
    # =====================================
    # URLs DA API REST
    # =====================================
    path('api/', include(router.urls)),
    # URL: "/api/*"
    # Views: Todas as ViewSets da API
    # Gera automaticamente:
    # - GET /api/users/ → Lista usuários
    # - POST /api/users/ → Cria usuário
    # - GET /api/users/1/ → Detalhes usuário 1
    # - PUT /api/users/1/ → Atualiza usuário 1
    # - DELETE /api/users/1/ → Deleta usuário 1
    # E assim por diante para todos os modelos...
]

"""
FLUXO DE UMA REQUISIÇÃO:
========================
1. Usuário acessa URL (ex: "/dashboard/")
2. Django procura a URL em urlpatterns
3. Encontra: path('dashboard/', views.dashboard, name='dashboard')
4. Executa: views.dashboard(request)
5. A view processa a lógica
6. Retorna resposta (HTML, JSON, redirect, etc.)
7. Navegador exibe o resultado
"""

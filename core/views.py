"""
VIEWS.PY - Lógica de Negócio do Sistema Pulse
=============================================
Este arquivo contém toda a lógica que processa as requisições.
Quando o usuário clica em algo, uma view é executada.

ESTRUTURA:
1. Imports e utilitários
2. Views WEB (páginas HTML)
3. Views CRUD (criar/ler/atualizar/deletar)
4. Views API (endpoints REST)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Q, Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .forms import CustomUserCreationForm, AgendamentoForm, ProfissionalForm, ServicoForm
from .models import Agendamento, Profissional, Servico, User
from .serializers import UserSerializer, ProfissionalSerializer, ServicoSerializer, AgendamentoSerializer

# ==========================================
# UTILITÁRIOS - FUNÇÕES AUXILIARES
# ==========================================
def is_admin(user):
    """
    Verifica se o usuário é administrador.
    Usado para controlar acesso a páginas admin.
    """
    return user.role == 'admin'

# ==========================================
# VIEWS WEB - PÁGINAS DO SITE
# ==========================================

def home(request):
    """
    PÁGINA INICIAL ("/")
    
    LÓGICA:
    - Se usuário já está logado → vai para dashboard
    - Se não está logado → mostra página de boas-vindas
    """
    if request.user.is_authenticated:
        return redirect('core:consultorio_dashboard')
    return render(request, 'core/home.html')

def register(request):
    """
    PÁGINA DE CADASTRO ("/register/")
    
    LÓGICA:
    - GET: Mostra formulário vazio
    - POST: Processa dados e cria usuário
    """
    if request.method == 'POST':
        # Usuário enviou dados do formulário
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Dados válidos → criar usuário
            user = form.save()
            login(request, user)  # Já deixa logado
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('core:consultorio_dashboard')
    else:
        # Primeira visita → formulário vazio
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def agendar_consulta(request):
    """
    PÁGINA DE AGENDAMENTO ("/agendar/")
    
    LÓGICA:
    - GET: Mostra formulário de agendamento
    - POST: Salva novo agendamento
    """
    if request.method == 'POST':
        # Usuário enviou dados do agendamento
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            # Criar agendamento mas não salvar ainda
            agendamento = form.save(commit=False)
            # Definir que o paciente é o usuário logado
            agendamento.paciente = request.user
            # Agora sim salvar no banco
            agendamento.save()
            messages.success(request, 'Agendamento realizado com sucesso!')
            return redirect('core:consultorio_dashboard')
    else:
        # Primeira visita → formulário vazio
        form = AgendamentoForm()
    
    return render(request, 'core/agendar.html', {'form': form})

# ==========================================
# VIEWS CRUD - APENAS PARA ADMINISTRADORES
# ==========================================

@login_required
@user_passes_test(is_admin)  # Só admin pode acessar
def profissional_list(request):
    """
    LISTA DE PROFISSIONAIS ("/profissionais/")
    Mostra todos os médicos cadastrados.
    """
    profissionais = Profissional.objects.all()
    return render(request, 'core/profissional_list.html', {'profissionais': profissionais})

@login_required
@user_passes_test(is_admin)
def profissional_create(request):
    """
    CADASTRAR NOVO PROFISSIONAL ("/profissionais/novo/")
    Permite admin adicionar médicos ao sistema.
    """
    if request.method == 'POST':
        form = ProfissionalForm(request.POST)
        if form.is_valid():
            form.save()  # Salva direto no banco
            messages.success(request, 'Profissional cadastrado com sucesso!')
            return redirect('core:profissional_list')
    else:
        form = ProfissionalForm()
    
    return render(request, 'core/profissional_form.html', {
        'form': form, 
        'title': 'Cadastrar Profissional'
    })

@login_required
@user_passes_test(is_admin)
def servico_list(request):
    """
    LISTA DE SERVIÇOS ("/servicos/")
    Mostra todos os tipos de consulta disponíveis.
    """
    servicos = Servico.objects.all()
    return render(request, 'core/servico_list.html', {'servicos': servicos})

@login_required
@user_passes_test(is_admin)
def servico_create(request):
    """
    CADASTRAR NOVO SERVIÇO ("/servicos/novo/")
    Permite admin adicionar tipos de consulta.
    """
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
            return redirect('core:servico_list')
    else:
        form = ServicoForm()
    
    return render(request, 'core/servico_form.html', {
        'form': form, 
        'title': 'Cadastrar Serviço'
    })

@login_required
def agendamento_list(request):
    """
    LISTA DE AGENDAMENTOS ("/agendamentos/")
    
    LÓGICA:
    - Admin: Vê todos os agendamentos
    - Paciente: Vê apenas os seus
    """
    if request.user.role == 'admin':
        agendamentos = Agendamento.objects.all().order_by('-data_hora')
    else:
        agendamentos = Agendamento.objects.filter(paciente=request.user).order_by('-data_hora')
    
    return render(request, 'core/agendamento_list.html', {'agendamentos': agendamentos})

# ==========================================
# API VIEWSETS - ENDPOINTS REST
# ==========================================
# Estas views respondem em JSON para apps mobile ou frontend separado

class UserViewSet(viewsets.ModelViewSet):
    """
    API para usuários (/api/users/)
    
    ENDPOINTS GERADOS:
    - GET /api/users/ → Lista usuários
    - POST /api/users/ → Cria usuário
    - GET /api/users/1/ → Detalhes do usuário 1
    - PUT /api/users/1/ → Atualiza usuário 1
    - DELETE /api/users/1/ → Deleta usuário 1
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Só logados acessam

class ProfissionalViewSet(viewsets.ModelViewSet):
    """API para profissionais (/api/profissionais/)"""
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [permissions.IsAuthenticated]

class ServicoViewSet(viewsets.ModelViewSet):
    """API para serviços (/api/servicos/)"""
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAuthenticated]

class AgendamentoViewSet(viewsets.ModelViewSet):
    """
    API para agendamentos (/api/agendamentos/)
    
    REGRA ESPECIAL:
    - Admin vê todos os agendamentos
    - Paciente vê apenas os seus
    """
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Define quais agendamentos o usuário pode ver"""
        if self.request.user.role == 'admin':
            return Agendamento.objects.all()
        return Agendamento.objects.filter(paciente=self.request.user)
    
    def perform_create(self, serializer):
        """Ao criar agendamento via API, define o paciente automaticamente"""
        serializer.save(paciente=self.request.user)

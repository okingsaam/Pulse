from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta
from .models import User, Profissional, Servico, Agendamento
import json

def consultorio_pacientes(request):
    """Página de pacientes do consultório"""
    pacientes = User.objects.filter(role='cliente').order_by('-date_joined')
    
    context = {
        'pacientes': pacientes,
        'total_pacientes': pacientes.count(),
        'user': request.user if request.user.is_authenticated else {'username': 'Demo', 'first_name': 'Dr. Demo'},
    }
    
    return render(request, 'core/consultorio_pacientes.html', context)

def consultorio_agenda(request):
    """Página de agenda do consultório"""
    hoje = timezone.now().date()
    
    # Agendamentos da semana
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    agendamentos = Agendamento.objects.filter(
        data_hora__date__gte=inicio_semana,
        data_hora__date__lte=fim_semana
    ).order_by('data_hora')
    
    context = {
        'agendamentos': agendamentos,
        'hoje': hoje,
        'user': request.user if request.user.is_authenticated else {'username': 'Demo', 'first_name': 'Dr. Demo'},
    }
    
    return render(request, 'core/consultorio_agenda.html', context)

def consultorio_financeiro(request):
    """Página financeira do consultório"""
    hoje = timezone.now().date()
    mes_atual = hoje.replace(day=1)
    
    # Receita do mês
    agendamentos_mes = Agendamento.objects.filter(
        data_hora__date__gte=mes_atual,
        status='confirmado'
    )
    
    context = {
        'agendamentos_mes': agendamentos_mes,
        'total_agendamentos': agendamentos_mes.count(),
        'user': request.user if request.user.is_authenticated else {'username': 'Demo', 'first_name': 'Dr. Demo'},
    }
    
    return render(request, 'core/consultorio_financeiro.html', context)
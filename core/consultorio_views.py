from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import User, Profissional, Servico, Agendamento
import json

def consultorio_dashboard(request):
    """Dashboard principal do consultório médico"""
    
    # Estatísticas básicas
    total_pacientes = User.objects.filter(role='cliente').count()
    
    # Agendamentos de hoje
    hoje = timezone.now().date()
    agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje).count()
    
    # Aniversariantes do dia
    aniversariantes_hoje = User.objects.filter(
        role='cliente',
        date_joined__month=hoje.month,
        date_joined__day=hoje.day
    ).count()
    
    # Pacientes recentes (últimos 5)
    pacientes_recentes = User.objects.filter(role='cliente').order_by('-date_joined')[:5]
    
    # Sala de espera (agendamentos confirmados para hoje)
    sala_espera = Agendamento.objects.filter(
        data_hora__date=hoje,
        status='confirmado'
    ).count()
    
    # Dados para gráfico de consultas por mês (últimos 12 meses)
    consultas_por_mes = []
    meses_labels = []
    
    for i in range(11, -1, -1):
        data = timezone.now() - timedelta(days=30*i)
        mes_nome = data.strftime('%b')
        consultas_count = Agendamento.objects.filter(
            data_hora__year=data.year,
            data_hora__month=data.month,
            status='confirmado'
        ).count()
        
        meses_labels.append(mes_nome)
        consultas_por_mes.append(consultas_count)
    
    # Dados para gráfico de convênios (placeholder - você pode ajustar conforme seus dados)
    convenios_data = [45, 35, 20]  # Valores numéricos simples
    convenios_labels = ['Amil', 'Particular', 'Golden Cross']
    
    # Próximos agendamentos
    proximos_agendamentos = Agendamento.objects.filter(
        data_hora__gt=timezone.now(),
        status='confirmado'
    ).order_by('data_hora')[:5]
    
    context = {
        'total_pacientes': total_pacientes,
        'agendamentos_hoje': agendamentos_hoje,
        'aniversariantes_hoje': aniversariantes_hoje,
        'pacientes_recentes': pacientes_recentes,
        'sala_espera': sala_espera,
        'consultas_por_mes': consultas_por_mes,
        'meses_labels': meses_labels,
        'convenios_data': convenios_data,
        'convenios_labels': convenios_labels,
        'proximos_agendamentos': proximos_agendamentos,
        'user': request.user if request.user.is_authenticated else {'username': 'Demo', 'first_name': 'Dr. Demo'},
    }
    
    return render(request, 'core/consultorio_dashboard_fixed.html', context)
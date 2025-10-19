"""
REPORTS.PY - Sistema de Relatórios do Pulse
============================================
Funções para gerar relatórios e estatísticas
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Agendamento, Profissional, Servico, User
import json

def is_admin(user):
    """Verifica se o usuário é admin"""
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def relatorio_agendamentos(request):
    """Relatório de agendamentos por período"""
    # Filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    profissional_id = request.GET.get('profissional')
    status = request.GET.get('status')
    
    # Query base
    agendamentos = Agendamento.objects.select_related('paciente', 'servico', 'profissional')
    
    # Aplicar filtros
    if data_inicio:
        agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)
    if data_fim:
        agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)
    if profissional_id:
        agendamentos = agendamentos.filter(profissional_id=profissional_id)
    if status:
        agendamentos = agendamentos.filter(status=status)
    
    # Estatísticas
    total_agendamentos = agendamentos.count()
    agendamentos_confirmados = agendamentos.filter(status='confirmado').count()
    agendamentos_cancelados = agendamentos.filter(status='cancelado').count()
    
    # Dados para gráficos
    agendamentos_por_dia = agendamentos.extra(
        select={'dia': 'DATE(data_hora)'}
    ).values('dia').annotate(total=Count('id')).order_by('dia')
    
    agendamentos_por_profissional = agendamentos.values(
        'profissional__nome'
    ).annotate(total=Count('id')).order_by('-total')
    
    context = {
        'agendamentos': agendamentos.order_by('-data_hora')[:50],
        'total_agendamentos': total_agendamentos,
        'agendamentos_confirmados': agendamentos_confirmados,
        'agendamentos_cancelados': agendamentos_cancelados,
        'agendamentos_por_dia': list(agendamentos_por_dia),
        'agendamentos_por_profissional': list(agendamentos_por_profissional),
        'profissionais': Profissional.objects.all(),
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'profissional_id': profissional_id,
            'status': status,
        }
    }
    
    return render(request, 'core/relatorio_agendamentos.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_estatisticas(request):
    """API para dados do dashboard"""
    hoje = timezone.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    inicio_mes = hoje.replace(day=1)
    
    # Estatísticas gerais
    stats = {
        'agendamentos_hoje': Agendamento.objects.filter(data_hora__date=hoje).count(),
        'agendamentos_semana': Agendamento.objects.filter(data_hora__date__gte=inicio_semana).count(),
        'agendamentos_mes': Agendamento.objects.filter(data_hora__date__gte=inicio_mes).count(),
        'total_pacientes': User.objects.filter(role='paciente').count(),
        'total_profissionais': Profissional.objects.count(),
        'total_servicos': Servico.objects.count(),
    }
    
    # Agendamentos por status
    agendamentos_status = Agendamento.objects.values('status').annotate(
        total=Count('id')
    )
    
    # Profissionais mais procurados
    profissionais_populares = Agendamento.objects.values(
        'profissional__nome'
    ).annotate(total=Count('id')).order_by('-total')[:5]
    
    # Serviços mais procurados
    servicos_populares = Agendamento.objects.values(
        'servico__nome'
    ).annotate(total=Count('id')).order_by('-total')[:5]
    
    # Receita estimada do mês
    receita_mes = Agendamento.objects.filter(
        data_hora__date__gte=inicio_mes,
        status='confirmado'
    ).aggregate(
        total=Sum('servico__preco')
    )['total'] or 0
    
    data = {
        'stats': stats,
        'agendamentos_status': list(agendamentos_status),
        'profissionais_populares': list(profissionais_populares),
        'servicos_populares': list(servicos_populares),
        'receita_mes': float(receita_mes),
    }
    
    return JsonResponse(data)

@login_required
def agenda_semanal(request):
    """Agenda visual semanal"""
    # Calcular semana atual
    hoje = timezone.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    # Buscar agendamentos da semana
    agendamentos = Agendamento.objects.filter(
        data_hora__date__gte=inicio_semana,
        data_hora__date__lte=fim_semana
    ).select_related('paciente', 'servico', 'profissional').order_by('data_hora')
    
    # Organizar por dia
    agenda_semanal = {}
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        agenda_semanal[dia] = agendamentos.filter(data_hora__date=dia)
    
    context = {
        'agenda_semanal': agenda_semanal,
        'semana_atual': inicio_semana,
        'agendamentos': agendamentos,
    }
    
    return render(request, 'core/agenda_semanal.html', context)
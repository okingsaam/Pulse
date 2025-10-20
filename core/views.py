from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import date, timedelta
from .models import Paciente, Agendamento, Consulta, Profissional, Servico

def dashboard(request):
    """Dashboard principal com estatísticas"""
    hoje = timezone.now().date()
    mes_atual = hoje.replace(day=1)
    
    # Agendamentos de hoje
    agendamentos_hoje_lista = Agendamento.objects.filter(
        data_hora__date=hoje,
        status__in=['agendado', 'confirmado']
    ).select_related('paciente').order_by('data_hora')
    
    # Aniversariantes de hoje
    aniversariantes_hoje_lista = Paciente.objects.filter(
        ativo=True,
        data_nascimento__month=hoje.month,
        data_nascimento__day=hoje.day
    )
    
    # Contadores para agendamentos
    agendamentos_confirmados = Agendamento.objects.filter(
        data_hora__date=hoje,
        status='confirmado'
    ).count()
    
    # Consultas pagas no mês
    consultas_pagas = Consulta.objects.filter(
        criado_em__date__gte=mes_atual,
        pago=True
    ).count()
    
    # Pacientes novos no mês
    pacientes_novos_mes = Paciente.objects.filter(
        ativo=True,
        criado_em__date__gte=mes_atual
    ).count()
    
    context = {
        'total_pacientes': Paciente.objects.filter(ativo=True).count(),
        'agendamentos_hoje': agendamentos_hoje_lista.count(),
        'agendamentos_hoje_lista': agendamentos_hoje_lista[:10],  # Limita a 10 para o sidebar
        'agendamentos_confirmados': agendamentos_confirmados,
        'aniversariantes_hoje': aniversariantes_hoje_lista.count(),
        'aniversariantes_lista': aniversariantes_hoje_lista[:5],  # Limita a 5
        'consultas_mes': Consulta.objects.filter(
            criado_em__date__gte=mes_atual
        ).count(),
        'consultas_pagas': consultas_pagas,
        'pacientes_novos_mes': pacientes_novos_mes,
        'faturamento_mes': Consulta.objects.filter(
            criado_em__date__gte=mes_atual,
            pago=True
        ).aggregate(total=Sum('valor'))['total'] or 0,
        'proximos_agendamentos': Agendamento.objects.filter(
            data_hora__gte=timezone.now(),
            status__in=['agendado', 'confirmado']
        ).order_by('data_hora')[:5],
        'pacientes_recentes': Paciente.objects.filter(
            ativo=True
        ).order_by('-criado_em')[:5]
    }
    return render(request, 'core/consultorio_dashboard.html', context)

def agenda(request):
    """Página de agenda com agendamentos"""
    hoje = timezone.now().date()
    agendamentos_hoje = Agendamento.objects.filter(
        data_hora__date=hoje
    ).order_by('data_hora')
    
    proximos_agendamentos = Agendamento.objects.filter(
        data_hora__date__gt=hoje,
        status__in=['agendado', 'confirmado']
    ).order_by('data_hora')[:10]
    
    context = {
        'agendamentos_hoje': agendamentos_hoje,
        'proximos_agendamentos': proximos_agendamentos,
        'data_hoje': hoje,
    }
    return render(request, 'core/consultorio_agenda.html', context)

def pacientes(request):
    """Página de gestão de pacientes"""
    busca = request.GET.get('busca', '')
    
    pacientes_query = Paciente.objects.filter(ativo=True)
    
    if busca:
        pacientes_query = pacientes_query.filter(
            Q(nome__icontains=busca) |
            Q(cpf__icontains=busca) |
            Q(telefone__icontains=busca)
        )
    
    context = {
        'pacientes': pacientes_query.order_by('nome')[:50],  # Limita a 50 para performance
        'total_pacientes': Paciente.objects.filter(ativo=True).count(),
        'pacientes_novos_mes': Paciente.objects.filter(
            ativo=True,
            criado_em__date__gte=date.today().replace(day=1)
        ).count(),
        'busca': busca,
    }
    return render(request, 'core/consultorio_pacientes.html', context)

def financeiro(request):
    """Página de controle financeiro"""
    hoje = timezone.now().date()
    mes_atual = hoje.replace(day=1)
    
    # Consultas do mês
    consultas_mes = Consulta.objects.filter(
        criado_em__date__gte=mes_atual
    )
    
    # Estatísticas financeiras
    faturamento_total = consultas_mes.aggregate(
        total=Sum('valor')
    )['total'] or 0
    
    faturamento_pago = consultas_mes.filter(
        pago=True
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    faturamento_pendente = faturamento_total - faturamento_pago
    
    context = {
        'faturamento_total': faturamento_total,
        'faturamento_pago': faturamento_pago,
        'faturamento_pendente': faturamento_pendente,
        'consultas_pagas': consultas_mes.filter(pago=True).count(),
        'consultas_pendentes': consultas_mes.filter(pago=False).count(),
        'consultas_recentes': consultas_mes.order_by('-criado_em')[:10],
    }
    return render(request, 'core/consultorio_financeiro.html', context)
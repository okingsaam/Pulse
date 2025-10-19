"""
URLs para relatórios e funcionalidades avançadas
"""
from django.urls import path
from . import reports

app_name = 'reports'

urlpatterns = [
    path('semanal/', reports.agenda_semanal, name='agenda_semanal'),
    path('relatorio/', reports.relatorio_agendamentos, name='relatorio_agendamentos'),
    path('api/estatisticas/', reports.dashboard_estatisticas, name='dashboard_estatisticas'),
]
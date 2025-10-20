from django.contrib import admin
from .models import Paciente, Profissional, Agendamento, Consulta, Servico

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'telefone', 'idade', 'ativo', 'criado_em']
    list_filter = ['ativo', 'sexo', 'criado_em']
    search_fields = ['nome', 'cpf', 'telefone', 'email']
    list_editable = ['ativo']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cpf', 'rg', 'data_nascimento', 'sexo')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'endereco')
        }),
        ('Observações', {
            'fields': ('observacoes', 'ativo')
        }),
    )

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'especialidade', 'crm', 'telefone', 'ativo']
    list_filter = ['ativo', 'especialidade']
    search_fields = ['nome', 'crm', 'especialidade']
    list_editable = ['ativo']

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'profissional', 'data_hora', 'status']
    list_filter = ['status', 'profissional', 'data_hora']
    search_fields = ['paciente__nome', 'profissional__nome']
    list_editable = ['status']
    date_hierarchy = 'data_hora'

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['agendamento', 'valor', 'pago', 'criado_em']
    list_filter = ['pago', 'criado_em']
    search_fields = ['agendamento__paciente__nome']
    list_editable = ['pago']
    date_hierarchy = 'criado_em'

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'ativo', 'criado_em']
    list_filter = ['ativo']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo']
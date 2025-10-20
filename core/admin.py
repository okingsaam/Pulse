from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum
from django.utils import timezone
from django.contrib.admin import AdminSite
from django.shortcuts import render
from .models import User, Profissional, Servico, Agendamento

# Configurações globais do admin
admin.site.site_header = "🏥 Sistema Pulse - Gestão de Agendamentos"
admin.site.site_title = "Pulse Admin"
admin.site.index_title = "Painel de Controle"

# Customizar a view do index do admin
class PulseAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Adicionar estatísticas ao contexto
        extra_context.update({
            'user_count': User.objects.count(),
            'professional_count': Profissional.objects.count(),
            'service_count': Servico.objects.count(),
            'appointment_count': Agendamento.objects.count(),
        })
        
        return super().index(request, extra_context=extra_context)

# Usar o site admin customizado
# admin_site = PulseAdminSite(name='pulse_admin')
admin.site.site_title = "Pulse Admin"
admin.site.index_title = "Painel Administrativo"

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_staff', 'total_agendamentos', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    list_editable = ('role',)
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('role', 'phone'),
            'classes': ('wide',)
        }),
    )
    
    def total_agendamentos(self, obj):
        if obj.role == 'paciente':
            count = obj.agendamento_set.count()
            return format_html(
                '<span style="color: {};">{}</span>',
                'green' if count > 0 else 'gray',
                count
            )
        return '-'
    total_agendamentos.short_description = 'Total Agendamentos'

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade', 'total_servicos', 'total_agendamentos', 'status_badge')
    list_filter = ('especialidade',)
    search_fields = ('nome', 'especialidade')
    ordering = ('nome',)
    
    def total_servicos(self, obj):
        count = obj.servico_set.count()
        return format_html(
            '<span style="color: blue; font-weight: bold;">{}</span>',
            count
        )
    total_servicos.short_description = 'Serviços'
    
    def total_agendamentos(self, obj):
        count = Agendamento.objects.filter(profissional=obj).count()
        return format_html(
            '<span style="color: orange; font-weight: bold;">{}</span>',
            count
        )
    total_agendamentos.short_description = 'Agendamentos'
    
    def status_badge(self, obj):
        tem_servicos = obj.servico_set.exists()
        if tem_servicos:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 2px 8px; border-radius: 3px;">Ativo</span>'
            )
        return format_html(
            '<span style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 3px;">Inativo</span>'
        )
    status_badge.short_description = 'Status'

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'profissional', 'preco', 'duracao', 'total_agendamentos')
    list_filter = ('profissional', 'preco')
    search_fields = ('nome', 'descricao', 'profissional__nome')
    ordering = ('nome',)
    list_editable = ('preco',)
    
    def preco_formatado(self, obj):
        return format_html(
            '<span style="color: green; font-weight: bold;">R$ {:.2f}</span>',
            obj.preco
        )
    preco_formatado.short_description = 'Preço'
    
    def total_agendamentos(self, obj):
        count = obj.agendamento_set.count()
        return format_html(
            '<span style="color: purple; font-weight: bold;">{}</span>',
            count
        )
    total_agendamentos.short_description = 'Agendamentos'

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('paciente_link', 'servico', 'profissional', 'data_hora_formatada', 'status', 'valor_total')
    list_filter = ('status', 'data_hora', 'profissional', 'servico')
    search_fields = ('paciente__username', 'paciente__first_name', 'paciente__last_name', 
                    'servico__nome', 'profissional__nome')
    date_hierarchy = 'data_hora'
    ordering = ('-data_hora',)
    list_editable = ('status',)
    
    actions = ['marcar_confirmado', 'marcar_cancelado']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('paciente', 'servico', 'profissional')
    
    def paciente_link(self, obj):
        url = reverse('admin:core_user_change', args=[obj.paciente.pk])
        return format_html(
            '<a href="{}" style="color: #007cba;">{}</a>',
            url, obj.paciente.username
        )
    paciente_link.short_description = 'Paciente'
    
    def data_hora_formatada(self, obj):
        agora = timezone.now()
        if obj.data_hora < agora:
            cor = '#dc3545'  # Vermelho para passado
        elif obj.data_hora <= agora + timezone.timedelta(days=1):
            cor = '#ffc107'  # Amarelo para próximo
        else:
            cor = '#28a745'  # Verde para futuro
            
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            cor, obj.data_hora.strftime('%d/%m/%Y %H:%M')
        )
    data_hora_formatada.short_description = 'Data/Hora'
    
    def status_badge(self, obj):
        cores = {
            'pendente': '#ffc107',
            'confirmado': '#28a745',
            'cancelado': '#dc3545'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
            cores.get(obj.status, '#6c757d'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def valor_total(self, obj):
        try:
            preco = float(obj.servico.preco) if obj.servico else 0
            return format_html(
                '<span style="color: green; font-weight: bold;">R$ {:.2f}</span>',
                preco
            )
        except (ValueError, AttributeError):
            return format_html(
                '<span style="color: red;">Erro no preço</span>'
            )
    valor_total.short_description = 'Valor'
    
    def marcar_confirmado(self, request, queryset):
        updated = queryset.update(status='confirmado')
        self.message_user(request, f'{updated} agendamento(s) confirmado(s).')
    marcar_confirmado.short_description = "Confirmar agendamentos selecionados"
    
    def marcar_cancelado(self, request, queryset):
        updated = queryset.update(status='cancelado')
        self.message_user(request, f'{updated} agendamento(s) cancelado(s).')
    marcar_cancelado.short_description = "Cancelar agendamentos selecionados"

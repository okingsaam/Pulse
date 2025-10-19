"""
Context processors para adicionar dados globais aos templates
"""
from .models import User, Profissional, Servico, Agendamento

def admin_stats(request):
    """
    Adiciona estatísticas do sistema ao contexto dos templates admin
    """
    if request.path.startswith('/admin/'):
        return {
            'user_count': User.objects.count(),
            'professional_count': Profissional.objects.count(),
            'service_count': Servico.objects.count(),
            'appointment_count': Agendamento.objects.count(),
        }
    return {}
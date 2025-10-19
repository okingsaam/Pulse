"""
Middleware personalizado para o sistema Pulse
"""
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class AdminOnlyMiddleware:
    """
    Middleware que restringe certas URLs apenas para admins
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs que só admins podem acessar
        self.admin_only_paths = [
            '/profissionais/',
            '/servicos/',
            '/agendamentos/',
        ]

    def __call__(self, request):
        # Verificar se a URL requer acesso admin
        if any(request.path.startswith(path) for path in self.admin_only_paths):
            if not request.user.is_authenticated:
                messages.warning(request, 'Você precisa fazer login para acessar esta página.')
                return redirect('core:login')
            elif request.user.role != 'admin':
                messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
                return redirect('core:dashboard')

        response = self.get_response(request)
        return response


class LoggingMiddleware:
    """
    Middleware para log de ações importantes
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log de tentativas de login
        if request.path == '/login/' and request.method == 'POST':
            username = request.POST.get('username', 'unknown')
            logger.info(f'Tentativa de login para usuário: {username} de IP: {request.META.get("REMOTE_ADDR")}')

        response = self.get_response(request)
        
        # Log de ações administrativas
        if request.user.is_authenticated and request.user.role == 'admin':
            if request.method in ['POST', 'PUT', 'DELETE']:
                logger.info(f'Admin {request.user.username} executou {request.method} em {request.path}')

        return response
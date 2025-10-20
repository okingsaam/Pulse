#!/usr/bin/env python3
"""
Teste Funcional Admin - Sistema Pulse
Testa todas as funcionalidades do Django Admin
"""

import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Profissional, Servico, Agendamento

User = get_user_model()

class AdminFunctionalTester:
    def __init__(self):
        self.client = Client()
        self.admin_user = None
        self.errors = []
        self.success_count = 0
        
    def log_success(self, message):
        print(f"✅ {message}")
        self.success_count += 1
        
    def log_error(self, message, exception=None):
        error_msg = f"❌ {message}"
        if exception:
            error_msg += f" | Erro: {str(exception)}"
        print(error_msg)
        self.errors.append(error_msg)
        
    def create_test_admin(self):
        """Cria usuário admin para testes"""
        try:
            # Verificar se já existe um admin
            admin_user = User.objects.filter(is_superuser=True).first()
            
            if admin_user:
                self.admin_user = admin_user
                self.log_success(f"Admin existente encontrado: {admin_user.username}")
            else:
                # Criar novo admin
                admin_user = User.objects.create_superuser(
                    username='admin_test',
                    email='admin@pulse.com',
                    password='admin123',
                    role='admin'
                )
                self.admin_user = admin_user
                self.log_success(f"Admin criado para teste: {admin_user.username}")
                
            return True
            
        except Exception as e:
            self.log_error("Erro ao criar admin de teste", e)
            return False
    
    def test_admin_login(self):
        """Testa login no admin"""
        try:
            # Fazer login
            login_successful = self.client.login(
                username=self.admin_user.username,
                password='admin123'
            )
            
            if login_successful:
                self.log_success("Login no admin realizado com sucesso")
                
                # Testar acesso à página principal do admin
                response = self.client.get('/admin/')
                
                if response.status_code == 200:
                    self.log_success("Página principal do admin acessível")
                else:
                    self.log_error(f"Página admin retornou status {response.status_code}")
                    
            else:
                self.log_error("Falha no login do admin")
                
        except Exception as e:
            self.log_error("Erro no teste de login admin", e)
    
    def test_admin_models_access(self):
        """Testa acesso aos models no admin"""
        models_to_test = [
            ('core', 'profissional', 'Profissional'),
            ('core', 'servico', 'Serviço'),
            ('core', 'agendamento', 'Agendamento'),
            ('core', 'user', 'Usuário'),
        ]
        
        for app, model, name in models_to_test:
            try:
                # Testar listagem
                url = f'/admin/{app}/{model}/'
                response = self.client.get(url)
                
                if response.status_code == 200:
                    self.log_success(f"Listagem de {name} acessível")
                else:
                    self.log_error(f"Erro ao acessar listagem de {name} - Status {response.status_code}")
                
                # Testar página de adicionar
                add_url = f'/admin/{app}/{model}/add/'
                response = self.client.get(add_url)
                
                if response.status_code == 200:
                    self.log_success(f"Página de adicionar {name} acessível")
                else:
                    self.log_error(f"Erro ao acessar página de adicionar {name} - Status {response.status_code}")
                    
            except Exception as e:
                self.log_error(f"Erro ao testar admin de {name}", e)
    
    def test_admin_crud_operations(self):
        """Testa operações CRUD no admin"""
        try:
            # Teste: Criar Profissional
            profissional_data = {
                'nome': 'Dr. Teste Admin',
                'especialidade': 'Clínica Geral',
                'crm': 'CRM123456',
                'telefone': '(11) 99999-9999',
                'email': 'dr.teste@pulse.com'
            }
            
            response = self.client.post('/admin/core/profissional/add/', profissional_data)
            
            if response.status_code in [200, 302]:
                self.log_success("Criação de Profissional via admin funcionando")
                
                # Verificar se foi criado
                profissional = Profissional.objects.filter(nome='Dr. Teste Admin').first()
                if profissional:
                    self.log_success("Profissional salvo no banco de dados")
                    
                    # Testar edição
                    edit_url = f'/admin/core/profissional/{profissional.id}/change/'
                    response = self.client.get(edit_url)
                    
                    if response.status_code == 200:
                        self.log_success("Página de edição de Profissional acessível")
                    
                    # Limpar dados de teste
                    profissional.delete()
                    self.log_success("Dados de teste limpos")
                    
            else:
                self.log_error(f"Erro ao criar Profissional - Status {response.status_code}")
                
        except Exception as e:
            self.log_error("Erro no teste CRUD admin", e)
    
    def test_admin_filters_and_search(self):
        """Testa filtros e busca no admin"""
        try:
            # Testar filtros na listagem de profissionais
            url = '/admin/core/profissional/?especialidade__exact=Cardiologia'
            response = self.client.get(url)
            
            if response.status_code == 200:
                self.log_success("Filtros do admin funcionando")
            else:
                self.log_error(f"Erro nos filtros admin - Status {response.status_code}")
            
            # Testar busca
            search_url = '/admin/core/profissional/?q=Dr'
            response = self.client.get(search_url)
            
            if response.status_code == 200:
                self.log_success("Busca no admin funcionando")
            else:
                self.log_error(f"Erro na busca admin - Status {response.status_code}")
                
        except Exception as e:
            self.log_error("Erro no teste de filtros/busca admin", e)
    
    def test_admin_theme(self):
        """Testa se o tema personalizado está aplicado"""
        try:
            response = self.client.get('/admin/')
            
            if response.status_code == 200:
                content = response.content.decode()
                
                # Verificar se o CSS customizado está sendo carregado
                if 'pulse_admin.css' in content:
                    self.log_success("CSS personalizado do admin carregado")
                else:
                    self.log_error("CSS personalizado não encontrado no admin")
                
                # Verificar cores roxas no HTML
                if '#8e44ad' in content or 'pulse-primary' in content:
                    self.log_success("Tema roxo aplicado no admin")
                else:
                    # Verificar no CSS estático
                    css_response = self.client.get('/static/admin/css/pulse_admin.css')
                    if css_response.status_code == 200:
                        self.log_success("Arquivo CSS do tema acessível")
                    
        except Exception as e:
            self.log_error("Erro no teste do tema admin", e)
    
    def test_admin_permissions(self):
        """Testa permissões do admin"""
        try:
            # Verificar se o admin tem todas as permissões necessárias
            if self.admin_user.is_superuser:
                self.log_success("Admin tem permissões de superusuário")
            else:
                self.log_error("Admin não tem permissões adequadas")
                
            # Testar acesso às configurações do admin
            response = self.client.get('/admin/auth/group/')
            
            if response.status_code == 200:
                self.log_success("Acesso a grupos de usuários funcionando")
            
        except Exception as e:
            self.log_error("Erro no teste de permissões admin", e)
    
    def run_all_tests(self):
        """Executa todos os testes do admin"""
        print("🔐 TESTE FUNCIONAL DO DJANGO ADMIN")
        print("=" * 60)
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        # Criar admin de teste
        if not self.create_test_admin():
            print("❌ Não foi possível criar admin de teste - abortando")
            return False
        
        # Lista de testes
        tests = [
            self.test_admin_login,
            self.test_admin_models_access,
            self.test_admin_crud_operations,
            self.test_admin_filters_and_search,
            self.test_admin_theme,
            self.test_admin_permissions,
        ]
        
        # Executar testes
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_error(f"Erro crítico no teste {test.__name__}", e)
        
        # Relatório final
        self.generate_report()
        
        return len(self.errors) == 0
    
    def generate_report(self):
        """Gera relatório final"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO DO TESTE ADMIN")
        print("=" * 60)
        
        total_checks = self.success_count + len(self.errors)
        success_rate = (self.success_count / total_checks * 100) if total_checks > 0 else 0
        
        print(f"✅ Sucessos: {self.success_count}")
        print(f"❌ Erros: {len(self.errors)}")
        print(f"📊 Taxa de sucesso: {success_rate:.1f}%")
        
        if self.errors:
            print("\n🚨 ERROS ENCONTRADOS:")
            for error in self.errors:
                print(f"  • {error}")
        
        print("\n" + "=" * 60)
        
        if len(self.errors) == 0:
            print("🎉 ADMIN DJANGO 100% FUNCIONAL!")
            print("✅ Todas as funcionalidades testadas com sucesso")
        else:
            print("⚠️  Admin tem problemas que precisam ser corrigidos")

def main():
    """Função principal"""
    tester = AdminFunctionalTester()
    success = tester.run_all_tests()
    
    if success:
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
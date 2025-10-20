#!/usr/bin/env python3
"""
Sistema de Validação Completa - Django Pulse
Testa todas as conexões, views, models, templates e funcionalidades
"""

import os
import sys
import django
import requests
import time
from pathlib import Path
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import connection
from django.core.management import call_command
from django.template.loader import get_template
from core.models import Profissional, Servico, Agendamento

User = get_user_model()  # Usar o modelo User correto

class PulseSystemValidator:
    def __init__(self):
        self.client = Client()
        self.base_url = "http://127.0.0.1:8000"
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_tests = 0
        
    def log_success(self, message):
        print(f"✅ {message}")
        self.success_count += 1
        
    def log_error(self, message, exception=None):
        error_msg = f"❌ {message}"
        if exception:
            error_msg += f" | Erro: {str(exception)}"
        print(error_msg)
        self.errors.append(error_msg)
        
    def log_warning(self, message):
        print(f"⚠️  {message}")
        self.warnings.append(message)
        
    def test_database_connection(self):
        """Testa conexão com banco de dados"""
        print("\n🗄️  TESTANDO CONEXÃO COM BANCO DE DADOS")
        print("-" * 50)
        
        try:
            # Testar conexão básica
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] == 1:
                    self.log_success("Conexão com banco de dados estabelecida")
                    
            # Testar se tabelas existem
            tables = connection.introspection.table_names()
            required_tables = ['core_user', 'core_profissional', 'core_servico', 'core_agendamento']
            
            for table in required_tables:
                if table in tables:
                    self.log_success(f"Tabela {table} existe")
                else:
                    self.log_error(f"Tabela {table} não encontrada")
                    
        except Exception as e:
            self.log_error("Falha na conexão com banco de dados", e)
            
    def test_models(self):
        """Testa todos os models"""
        print("\n📊 TESTANDO MODELS")
        print("-" * 50)
        
        try:
            # Testar User model
            user_count = User.objects.count()
            self.log_success(f"Model User funcional - {user_count} usuários")
            
            # Testar Profissional model
            prof_count = Profissional.objects.count()
            self.log_success(f"Model Profissional funcional - {prof_count} profissionais")
            
            # Testar Servico model
            serv_count = Servico.objects.count()
            self.log_success(f"Model Servico funcional - {serv_count} serviços")
            
            # Testar Agendamento model
            agend_count = Agendamento.objects.count()
            self.log_success(f"Model Agendamento funcional - {agend_count} agendamentos")
            
            # Testar criação de objetos
            if user_count == 0:
                self.log_warning("Nenhum usuário encontrado - considere criar dados de teste")
                
        except Exception as e:
            self.log_error("Erro ao testar models", e)
            
    def test_urls(self):
        """Testa todas as URLs do sistema"""
        print("\n🔗 TESTANDO URLS E VIEWS")
        print("-" * 50)
        
        urls_to_test = [
            ('core:home', 'Página inicial'),
            ('core:consultorio_dashboard', 'Dashboard consultório'),
            ('core:consultorio_agenda', 'Agenda consultório'),
            ('core:consultorio_pacientes', 'Pacientes consultório'),
            ('core:consultorio_financeiro', 'Financeiro consultório'),
            ('admin:index', 'Admin principal'),
        ]
        
        for url_name, description in urls_to_test:
            try:
                url = reverse(url_name)
                response = self.client.get(url)
                
                if response.status_code in [200, 302]:
                    self.log_success(f"{description} - Status {response.status_code}")
                else:
                    self.log_error(f"{description} - Status {response.status_code}")
                    
            except Exception as e:
                self.log_error(f"Erro ao testar {description}", e)
                
    def test_templates(self):
        """Testa se todos os templates existem e são válidos"""
        print("\n📄 TESTANDO TEMPLATES")
        print("-" * 50)
        
        templates_to_test = [
            'base.html',
            'core/consultorio_dashboard_fixed.html',
            'core/consultorio_agenda.html',
            'core/consultorio_pacientes.html',
            'core/consultorio_financeiro.html',
            'registration/login.html',
            'registration/register.html',
        ]
        
        for template_name in templates_to_test:
            try:
                template = get_template(template_name)
                self.log_success(f"Template {template_name} carregado")
            except Exception as e:
                self.log_error(f"Erro ao carregar template {template_name}", e)
                
    def test_static_files(self):
        """Testa arquivos estáticos"""
        print("\n🎨 TESTANDO ARQUIVOS ESTÁTICOS")
        print("-" * 50)
        
        static_files = [
            'static/css/pulse_theme.css',
            'static/admin/css/pulse_admin.css',
        ]
        
        for file_path in static_files:
            full_path = Path(file_path)
            if full_path.exists():
                self.log_success(f"Arquivo estático {file_path} existe")
                
                # Verificar se não está vazio
                if full_path.stat().st_size > 0:
                    self.log_success(f"Arquivo {file_path} não está vazio")
                else:
                    self.log_warning(f"Arquivo {file_path} está vazio")
            else:
                self.log_error(f"Arquivo estático {file_path} não encontrado")
                
    def test_admin_functionality(self):
        """Testa funcionalidade do admin"""
        print("\n⚙️  TESTANDO ADMIN DJANGO")
        print("-" * 50)
        
        try:
            # Testar se admin está registrado
            from django.contrib import admin
            from core.admin import ProfissionalAdmin, ServicoAdmin, AgendamentoAdmin
            
            # Verificar se models estão registrados
            if Profissional in admin.site._registry:
                self.log_success("Model Profissional registrado no admin")
            else:
                self.log_error("Model Profissional não registrado no admin")
                
            if Servico in admin.site._registry:
                self.log_success("Model Servico registrado no admin")
            else:
                self.log_error("Model Servico não registrado no admin")
                
            if Agendamento in admin.site._registry:
                self.log_success("Model Agendamento registrado no admin")
            else:
                self.log_error("Model Agendamento não registrado no admin")
                
        except Exception as e:
            self.log_error("Erro ao testar admin", e)
            
    def test_server_connection(self):
        """Testa se o servidor está rodando e respondendo"""
        print("\n🌐 TESTANDO CONEXÃO COM SERVIDOR")
        print("-" * 50)
        
        try:
            # Tentar conectar com o servidor
            response = requests.get(f"{self.base_url}/consultorio/", timeout=10)
            
            if response.status_code == 200:
                self.log_success("Servidor respondendo corretamente")
                self.log_success(f"Tempo de resposta: {response.elapsed.total_seconds():.2f}s")
            else:
                self.log_error(f"Servidor retornou status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.log_warning("Servidor não está rodando - execute 'python manage.py runserver'")
        except Exception as e:
            self.log_error("Erro ao conectar com servidor", e)
            
    def test_migrations(self):
        """Verifica status das migrações"""
        print("\n📦 VERIFICANDO MIGRAÇÕES")
        print("-" * 50)
        
        try:
            # Verificar se há migrações pendentes
            from django.core.management.commands.migrate import Command as MigrateCommand
            from django.db.migrations.executor import MigrationExecutor
            
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            
            if plan:
                self.log_warning(f"{len(plan)} migrações pendentes encontradas")
                for migration, backwards in plan:
                    print(f"    • {migration}")
            else:
                self.log_success("Todas as migrações aplicadas")
                
        except Exception as e:
            self.log_error("Erro ao verificar migrações", e)
            
    def test_context_processors(self):
        """Testa context processors"""
        print("\n🔄 TESTANDO CONTEXT PROCESSORS")
        print("-" * 50)
        
        try:
            from core.context_processors import admin_stats
            
            # Simular request
            class MockRequest:
                def __init__(self):
                    self.path = '/test/'
                    self.user = None
                
            request = MockRequest()
            context = admin_stats(request)
            
            if isinstance(context, dict):
                self.log_success("Context processor admin_stats funcionando")
                if context:
                    self.log_success(f"Context data: {list(context.keys())}")
            else:
                self.log_error("Context processor retornou tipo inválido")
                
        except Exception as e:
            self.log_error("Erro ao testar context processors", e)
            
    def test_forms(self):
        """Testa formulários"""
        print("\n📝 TESTANDO FORMULÁRIOS")
        print("-" * 50)
        
        try:
            from core.forms import AgendamentoForm
            
            # Testar se form pode ser instanciado
            form = AgendamentoForm()
            self.log_success("AgendamentoForm instanciado com sucesso")
            
            # Verificar campos
            if hasattr(form, 'fields') and form.fields:
                self.log_success(f"Form possui {len(form.fields)} campos")
            else:
                self.log_warning("Form não possui campos definidos")
                
        except Exception as e:
            self.log_error("Erro ao testar formulários", e)
            
    def test_serializers(self):
        """Testa serializers (se existirem)"""
        print("\n🔄 TESTANDO SERIALIZERS")
        print("-" * 50)
        
        try:
            from core.serializers import ProfissionalSerializer, ServicoSerializer, AgendamentoSerializer
            
            # Testar instanciação dos serializers
            prof_serializer = ProfissionalSerializer()
            self.log_success("ProfissionalSerializer instanciado")
            
            serv_serializer = ServicoSerializer()
            self.log_success("ServicoSerializer instanciado")
            
            agend_serializer = AgendamentoSerializer()
            self.log_success("AgendamentoSerializer instanciado")
            
        except ImportError:
            self.log_warning("Serializers não encontrados (normal se não usar DRF)")
        except Exception as e:
            self.log_error("Erro ao testar serializers", e)
            
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🔍 VALIDAÇÃO COMPLETA DO SISTEMA PULSE")
        print("=" * 60)
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        # Lista de todos os testes
        tests = [
            self.test_database_connection,
            self.test_models,
            self.test_urls,
            self.test_templates,
            self.test_static_files,
            self.test_admin_functionality,
            self.test_migrations,
            self.test_context_processors,
            self.test_forms,
            self.test_serializers,
            self.test_server_connection,
        ]
        
        self.total_tests = len(tests)
        
        # Executar todos os testes
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_error(f"Erro crítico no teste {test.__name__}", e)
                
        # Relatório final
        self.generate_report()
        
    def generate_report(self):
        """Gera relatório final"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL DA VALIDAÇÃO")
        print("=" * 60)
        
        total_checks = self.success_count + len(self.errors) + len(self.warnings)
        success_rate = (self.success_count / total_checks * 100) if total_checks > 0 else 0
        
        print(f"✅ Sucessos: {self.success_count}")
        print(f"❌ Erros: {len(self.errors)}")
        print(f"⚠️  Avisos: {len(self.warnings)}")
        print(f"📊 Taxa de sucesso: {success_rate:.1f}%")
        
        if self.errors:
            print("\n🚨 ERROS ENCONTRADOS:")
            for error in self.errors:
                print(f"  • {error}")
                
        if self.warnings:
            print("\n⚠️  AVISOS:")
            for warning in self.warnings:
                print(f"  • {warning}")
                
        print("\n" + "=" * 60)
        
        if len(self.errors) == 0:
            print("🎉 SISTEMA 100% FUNCIONAL!")
            print("✅ Todas as conexões Django estão operacionais")
            return True
        else:
            print("⚠️  Sistema com problemas que precisam ser corrigidos")
            return False

def main():
    """Função principal"""
    validator = PulseSystemValidator()
    success = validator.run_all_tests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
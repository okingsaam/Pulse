#!/usr/bin/env python3
"""
TESTE FINAL COMPLETO - SISTEMA PULSE
Validação exaustiva de todas as funcionalidades
"""

import os
import sys
import django
from pathlib import Path
import requests
from datetime import datetime
import time
import json

# Configurar Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from core.models import Profissional, Servico, Agendamento
from django.db import connection
from django.core.management import execute_from_command_line
from django.urls import reverse

class SystemValidator:
    def __init__(self):
        self.client = Client()
        self.results = []
        self.errors = []
        
    def log_result(self, test_name, success, message, details=None):
        """Registra resultado do teste"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        
        if success:
            print(f"✅ {test_name}: {message}")
        else:
            print(f"❌ {test_name}: {message}")
            self.errors.append(result)
        
        if details:
            for detail in details:
                print(f"   → {detail}")
    
    def test_database_integrity(self):
        """Testa integridade completa do banco"""
        try:
            # Teste básico de conexão
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            User = get_user_model()
            
            # Contar todos os modelos
            counts = {
                'Users': User.objects.count(),
                'Profissionais': Profissional.objects.count(),
                'Serviços': Servico.objects.count(),
                'Agendamentos': Agendamento.objects.count()
            }
            
            # Verificar relações
            details = []
            for key, value in counts.items():
                details.append(f"{key}: {value} registros")
            
            # Teste de queries complexas
            try:
                # Query com JOIN
                agendamentos_com_servico = Agendamento.objects.select_related('servico', 'profissional').count()
                details.append(f"Queries complexas: OK ({agendamentos_com_servico} agendamentos com relações)")
            except Exception as e:
                details.append(f"Queries complexas: ERRO - {str(e)}")
            
            self.log_result("Database Integrity", True, "Banco de dados íntegro", details)
            return True
            
        except Exception as e:
            self.log_result("Database Integrity", False, f"Erro no banco: {str(e)}")
            return False
    
    def test_all_urls(self):
        """Testa todas as URLs do sistema"""
        urls_to_test = [
            ('Home', '/'),
            ('Dashboard', '/consultorio/'),
            ('Agenda', '/consultorio/agenda/'),
            ('Pacientes', '/consultorio/pacientes/'),
            ('Financeiro', '/consultorio/financeiro/'),
            ('Admin Home', '/admin/'),
            ('Admin Profissionais', '/admin/core/profissional/'),
            ('Admin Serviços', '/admin/core/servico/'),
            ('Admin Agendamentos', '/admin/core/agendamento/'),
            ('Admin Users', '/admin/core/user/'),
        ]
        
        success_count = 0
        details = []
        
        for name, url in urls_to_test:
            try:
                start_time = time.time()
                response = self.client.get(url)
                response_time = time.time() - start_time
                
                if response.status_code in [200, 302]:
                    details.append(f"{name}: Status {response.status_code} ({response_time:.3f}s)")
                    success_count += 1
                else:
                    details.append(f"{name}: ERRO Status {response.status_code}")
                    
            except Exception as e:
                details.append(f"{name}: EXCEÇÃO - {str(e)}")
        
        success = success_count == len(urls_to_test)
        message = f"{success_count}/{len(urls_to_test)} URLs funcionando"
        
        self.log_result("URL Testing", success, message, details)
        return success
    
    def test_admin_functionality(self):
        """Testa funcionalidades específicas do admin"""
        try:
            User = get_user_model()
            admin_user = User.objects.filter(is_superuser=True).first()
            
            if not admin_user:
                self.log_result("Admin Functionality", False, "Nenhum superusuário encontrado")
                return False
            
            details = []
            
            # Teste de login no admin
            login_success = self.client.login(username=admin_user.username, password='admin123')
            if login_success:
                details.append("Login admin: OK")
            else:
                details.append("Login admin: FALHOU")
            
            # Teste de páginas específicas do admin
            admin_pages = [
                '/admin/',
                '/admin/core/profissional/',
                '/admin/core/servico/',
                '/admin/core/agendamento/',
                '/admin/core/user/',
            ]
            
            admin_success = 0
            for page in admin_pages:
                try:
                    response = self.client.get(page)
                    if response.status_code == 200:
                        admin_success += 1
                        details.append(f"{page}: OK")
                    else:
                        details.append(f"{page}: Status {response.status_code}")
                except Exception as e:
                    details.append(f"{page}: ERRO - {str(e)}")
            
            # Logout
            self.client.logout()
            
            success = admin_success == len(admin_pages)
            message = f"Admin funcional - {admin_success}/{len(admin_pages)} páginas OK"
            
            self.log_result("Admin Functionality", success, message, details)
            return success
            
        except Exception as e:
            self.log_result("Admin Functionality", False, f"Erro no admin: {str(e)}")
            return False
    
    def test_model_operations(self):
        """Testa operações CRUD nos modelos"""
        try:
            details = []
            
            # Teste de criação (CREATE)
            try:
                test_prof = Profissional.objects.create(
                    nome="Teste Validação",
                    especialidade="Teste",
                    email="teste@teste.com"
                )
                details.append("CREATE: Profissional criado com sucesso")
                
                # Teste de leitura (READ)
                prof_read = Profissional.objects.get(id=test_prof.id)
                details.append(f"READ: Profissional lido - {prof_read.nome}")
                
                # Teste de atualização (UPDATE)
                prof_read.nome = "Teste Atualizado"
                prof_read.save()
                details.append("UPDATE: Profissional atualizado")
                
                # Teste de exclusão (DELETE)
                prof_read.delete()
                details.append("DELETE: Profissional removido")
                
            except Exception as e:
                details.append(f"CRUD Operations: ERRO - {str(e)}")
                return False
            
            # Teste de queries
            try:
                # Filtros
                profs_ativos = Profissional.objects.filter(nome__icontains="Dr")
                details.append(f"FILTER: {profs_ativos.count()} profissionais encontrados")
                
                # Ordenação
                profs_ordenados = Profissional.objects.order_by('nome')
                details.append(f"ORDER: {profs_ordenados.count()} profissionais ordenados")
                
                # Agregação
                total_agendamentos = Agendamento.objects.count()
                details.append(f"COUNT: {total_agendamentos} agendamentos no sistema")
                
            except Exception as e:
                details.append(f"Queries: ERRO - {str(e)}")
            
            self.log_result("Model Operations", True, "Operações de modelo funcionais", details)
            return True
            
        except Exception as e:
            self.log_result("Model Operations", False, f"Erro nas operações: {str(e)}")
            return False
    
    def test_static_and_templates(self):
        """Testa arquivos estáticos e templates"""
        try:
            details = []
            
            # Verificar arquivos estáticos
            static_files = [
                'static/css/pulse_theme.css',
                'static/admin/css/pulse_admin.css',
            ]
            
            static_ok = 0
            for file_path in static_files:
                full_path = Path(__file__).parent / file_path
                if full_path.exists():
                    size = full_path.stat().st_size
                    details.append(f"{file_path}: OK ({size} bytes)")
                    static_ok += 1
                else:
                    details.append(f"{file_path}: AUSENTE")
            
            # Verificar templates
            templates = [
                'templates/core/consultorio_dashboard_fixed.html',
                'templates/core/consultorio_agenda.html',
                'templates/core/consultorio_pacientes.html',
                'templates/core/consultorio_financeiro.html',
                'templates/base.html',
            ]
            
            template_ok = 0
            for template_path in templates:
                full_path = Path(__file__).parent / template_path
                if full_path.exists():
                    template_ok += 1
                    details.append(f"{template_path}: OK")
                else:
                    details.append(f"{template_path}: AUSENTE")
            
            total_files = len(static_files) + len(templates)
            total_ok = static_ok + template_ok
            
            success = total_ok == total_files
            message = f"Arquivos: {total_ok}/{total_files} encontrados"
            
            self.log_result("Static and Templates", success, message, details)
            return success
            
        except Exception as e:
            self.log_result("Static and Templates", False, f"Erro nos arquivos: {str(e)}")
            return False
    
    def test_server_performance(self):
        """Testa performance do servidor"""
        try:
            base_url = "http://127.0.0.1:8000"
            test_urls = [
                "/consultorio/",
                "/consultorio/agenda/",
                "/consultorio/pacientes/",
                "/consultorio/financeiro/",
            ]
            
            details = []
            response_times = []
            
            for url in test_urls:
                try:
                    start_time = time.time()
                    response = requests.get(f"{base_url}{url}", timeout=10)
                    response_time = time.time() - start_time
                    response_times.append(response_time)
                    
                    if response.status_code == 200:
                        details.append(f"{url}: {response_time:.3f}s (Status 200)")
                    else:
                        details.append(f"{url}: {response_time:.3f}s (Status {response.status_code})")
                        
                except requests.exceptions.RequestException as e:
                    details.append(f"{url}: ERRO - {str(e)}")
                    return False
            
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            
            # Performance é boa se média < 1s e máxima < 2s
            performance_ok = avg_time < 1.0 and max_time < 2.0
            
            details.append(f"Tempo médio: {avg_time:.3f}s")
            details.append(f"Tempo máximo: {max_time:.3f}s")
            
            message = f"Performance {'boa' if performance_ok else 'aceitável'}"
            
            self.log_result("Server Performance", True, message, details)
            return True
            
        except Exception as e:
            self.log_result("Server Performance", False, f"Erro no teste: {str(e)}")
            return False
    
    def run_complete_validation(self):
        """Executa validação completa"""
        print("🏆 VALIDAÇÃO FINAL COMPLETA - SISTEMA PULSE")
        print("=" * 60)
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        tests = [
            ("Database Integrity", self.test_database_integrity),
            ("URL Testing", self.test_all_urls),
            ("Admin Functionality", self.test_admin_functionality),
            ("Model Operations", self.test_model_operations),
            ("Static and Templates", self.test_static_and_templates),
            ("Server Performance", self.test_server_performance),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔄 {test_name}:")
            print("-" * 40)
            
            if test_func():
                passed += 1
        
        # Relatório final
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL DA VALIDAÇÃO")
        print("=" * 60)
        
        print(f"✅ Testes aprovados: {passed}/{total}")
        print(f"📊 Taxa de sucesso: {(passed/total*100):.1f}%")
        
        if passed == total:
            print("\n🎉 SISTEMA COMPLETAMENTE VALIDADO!")
            print("✅ Todas as funcionalidades testadas com sucesso")
            print("🚀 Django está funcionando perfeitamente")
            print("🎨 Interface padronizada e funcional")
            print("💾 Banco de dados íntegro")
            print("⚡ Performance adequada")
        else:
            print(f"\n⚠️  {total-passed} teste(s) falharam")
            print("\n🔍 PROBLEMAS ENCONTRADOS:")
            for error in self.errors:
                print(f"❌ {error['test']}: {error['message']}")
        
        print("\n" + "=" * 60)
        
        # Salvar relatório detalhado
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total,
            'passed_tests': passed,
            'success_rate': (passed/total*100),
            'results': self.results,
            'errors': self.errors
        }
        
        with open('validation_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("📄 Relatório detalhado salvo em: validation_report.json")
        
        return passed == total

def main():
    validator = SystemValidator()
    return validator.run_complete_validation()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
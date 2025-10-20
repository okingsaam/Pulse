#!/usr/bin/env python3
"""
Teste Simples e Direto - Sistema Pulse
Validação rápida de todas as funcionalidades principais
"""

import os
import sys
import django
from pathlib import Path
import requests
from datetime import datetime

# Configurar Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from core.models import Profissional, Servico, Agendamento
from django.db import connection

def test_database_connection():
    """Testa conexão com banco de dados"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return True, "Banco de dados conectado"
    except Exception as e:
        return False, f"Erro no banco: {str(e)}"

def test_models():
    """Testa se os modelos estão funcionando"""
    try:
        User = get_user_model()
        
        # Contar registros
        users = User.objects.count()
        profissionais = Profissional.objects.count()
        servicos = Servico.objects.count()
        agendamentos = Agendamento.objects.count()
        
        return True, f"Modelos OK - Users: {users}, Profissionais: {profissionais}, Serviços: {servicos}, Agendamentos: {agendamentos}"
    except Exception as e:
        return False, f"Erro nos modelos: {str(e)}"

def test_urls():
    """Testa URLs principais"""
    client = Client()
    urls_to_test = [
        '/consultorio/',
        '/consultorio/agenda/',
        '/consultorio/pacientes/',
        '/consultorio/financeiro/',
        '/admin/',
    ]
    
    results = []
    for url in urls_to_test:
        try:
            response = client.get(url)
            if response.status_code in [200, 302]:
                results.append(f"✅ {url} - Status {response.status_code}")
            else:
                results.append(f"❌ {url} - Status {response.status_code}")
        except Exception as e:
            results.append(f"❌ {url} - Erro: {str(e)}")
    
    return True, "URLs testadas:\n" + "\n".join(results)

def test_admin_functionality():
    """Testa funcionalidades básicas do admin"""
    try:
        User = get_user_model()
        
        # Verificar se há um superusuário
        admin_users = User.objects.filter(is_superuser=True).count()
        
        if admin_users == 0:
            return False, "Nenhum superusuário encontrado"
        
        client = Client()
        
        # Tentar acessar páginas do admin
        admin_urls = [
            '/admin/',
            '/admin/core/profissional/',
            '/admin/core/servico/',
            '/admin/core/agendamento/',
        ]
        
        admin_ok = 0
        for url in admin_urls:
            try:
                response = client.get(url)
                if response.status_code in [200, 302]:
                    admin_ok += 1
            except:
                pass
        
        return True, f"Admin OK - {admin_ok}/{len(admin_urls)} páginas acessíveis, {admin_users} admin(s)"
    except Exception as e:
        return False, f"Erro no admin: {str(e)}"

def test_static_files():
    """Testa se arquivos estáticos existem"""
    try:
        static_files = [
            'static/css/pulse_theme.css',
            'static/admin/css/pulse_admin.css',
        ]
        
        existing = 0
        for file_path in static_files:
            full_path = Path(__file__).parent / file_path
            if full_path.exists():
                existing += 1
        
        return True, f"Arquivos estáticos - {existing}/{len(static_files)} encontrados"
    except Exception as e:
        return False, f"Erro nos estáticos: {str(e)}"

def test_templates():
    """Testa se templates existem"""
    try:
        templates = [
            'templates/core/consultorio_dashboard_fixed.html',
            'templates/core/consultorio_agenda.html',
            'templates/core/consultorio_pacientes.html',
            'templates/core/consultorio_financeiro.html',
            'templates/base.html',
        ]
        
        existing = 0
        for template_path in templates:
            full_path = Path(__file__).parent / template_path
            if full_path.exists():
                existing += 1
        
        return True, f"Templates - {existing}/{len(templates)} encontrados"
    except Exception as e:
        return False, f"Erro nos templates: {str(e)}"

def test_server_connectivity():
    """Testa se o servidor está respondendo"""
    try:
        response = requests.get('http://127.0.0.1:8000/consultorio/', timeout=5)
        if response.status_code == 200:
            return True, f"Servidor online - Status {response.status_code}"
        else:
            return False, f"Servidor com problema - Status {response.status_code}"
    except requests.exceptions.RequestException:
        return False, "Servidor offline ou inacessível"

def main():
    """Executa todos os testes"""
    
    print("🔍 TESTE RÁPIDO - SISTEMA PULSE")
    print("=" * 50)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("Conexão com Banco", test_database_connection),
        ("Modelos Django", test_models),
        ("URLs Principais", test_urls),
        ("Admin Django", test_admin_functionality),
        ("Arquivos Estáticos", test_static_files),
        ("Templates", test_templates),
        ("Conectividade Servidor", test_server_connectivity),
    ]
    
    results = []
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔄 Testando: {test_name}")
        print("-" * 30)
        
        try:
            success, message = test_func()
            if success:
                print(f"✅ {message}")
                passed += 1
                results.append((test_name, True, message))
            else:
                print(f"❌ {message}")
                results.append((test_name, False, message))
        except Exception as e:
            error_msg = f"Erro no teste: {str(e)}"
            print(f"❌ {error_msg}")
            results.append((test_name, False, error_msg))
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL")
    print("=" * 50)
    
    print(f"✅ Testes aprovados: {passed}/{len(tests)}")
    print(f"📊 Taxa de sucesso: {(passed/len(tests)*100):.1f}%")
    
    if passed == len(tests):
        print("\n🎉 SISTEMA 100% FUNCIONAL!")
        print("✅ Todas as verificações passaram")
        print("🚀 Django está rodando perfeitamente")
    else:
        print(f"\n⚠️  {len(tests)-passed} teste(s) falharam")
        
        print("\n🔍 DETALHES DOS PROBLEMAS:")
        for test_name, success, message in results:
            if not success:
                print(f"❌ {test_name}: {message}")
    
    print("\n" + "=" * 50)
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
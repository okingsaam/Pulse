#!/usr/bin/env python
"""
Script para iniciar o servidor Django com melhor estabilidade
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def start_server():
    """Inicia o servidor Django com configurações otimizadas"""
    
    # Configurar ambiente
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
    
    # Verificar se está no diretório correto
    if not Path('manage.py').exists():
        print("❌ Erro: execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    print("🚀 Iniciando servidor Pulse...")
    print("📍 URL: http://127.0.0.1:8000/")
    print("🏥 Interface médica: http://127.0.0.1:8000/consultorio/")
    print("⭐ Para parar: Ctrl+C")
    print("-" * 50)
    
    try:
        # Executar migrations se necessário
        print("🔄 Verificando migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate', '--run-syncdb'], 
                      check=False, capture_output=True)
        
        # Coletar arquivos estáticos
        print("📁 Coletando arquivos estáticos...")
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                      check=False, capture_output=True)
        
        # Iniciar servidor
        print("✅ Servidor iniciado com sucesso!")
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', 
            '127.0.0.1:8000',
            '--insecure'  # Para servir arquivos estáticos em desenvolvimento
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        print("💡 Tente: python manage.py runserver")

if __name__ == '__main__':
    start_server()
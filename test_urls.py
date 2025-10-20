#!/usr/bin/env python
"""
Script para testar todas as URLs do sistema
"""
import requests
import time

def test_urls():
    """Testar todas as URLs importantes"""
    base_url = "http://127.0.0.1:8000"
    
    urls_to_test = [
        "/",
        "/consultorio/dashboard/",
        "/consultorio/agenda/",
        "/consultorio/pacientes/",
        "/consultorio/financeiro/",
        "/admin/",
    ]
    
    print("🧪 Testando URLs do sistema...\n")
    
    for url in urls_to_test:
        try:
            response = requests.get(f"{base_url}{url}", timeout=5)
            status_icon = "✅" if response.status_code == 200 else "⚠️" if response.status_code in [301, 302] else "❌"
            print(f"{status_icon} {url} - Status: {response.status_code}")
            
            if response.status_code == 500:
                print(f"   💀 Erro 500 - Problema interno no servidor")
            elif response.status_code == 404:
                print(f"   🔍 Erro 404 - URL não encontrada")
            elif response.status_code in [301, 302]:
                print(f"   🔄 Redirecionamento para: {response.headers.get('Location', 'N/A')}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {url} - Erro de conexão: {e}")
        
        time.sleep(0.1)  # Pequena pausa entre requests
    
    print("\n🎯 Teste de URLs concluído!")

if __name__ == "__main__":
    test_urls()
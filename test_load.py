#!/usr/bin/env python3
"""
Teste de Carga e Performance - Sistema Pulse
Testa multiple requests e performance do sistema
"""

import time
import requests
import concurrent.futures
import statistics
from datetime import datetime

class PulseLoadTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.results = []
        
    def test_single_request(self, url):
        """Testa uma única requisição"""
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            return {
                'url': url,
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'success': response.status_code < 400,
                'size': len(response.content) if response.content else 0
            }
        except Exception as e:
            end_time = time.time()
            return {
                'url': url,
                'status_code': 0,
                'response_time': end_time - start_time,
                'success': False,
                'error': str(e),
                'size': 0
            }
    
    def test_concurrent_requests(self, urls, concurrent_users=5):
        """Testa requisições concorrentes"""
        print(f"\n🚀 TESTE DE CARGA - {concurrent_users} usuários simultâneos")
        print("-" * 50)
        
        all_requests = []
        for url in urls:
            all_requests.extend([url] * 3)  # 3 requests por URL
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            start_time = time.time()
            futures = [executor.submit(self.test_single_request, url) for url in all_requests]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            end_time = time.time()
            
        total_time = end_time - start_time
        successful_requests = sum(1 for r in results if r['success'])
        failed_requests = len(results) - successful_requests
        
        response_times = [r['response_time'] for r in results if r['success']]
        
        print(f"✅ Total de requisições: {len(results)}")
        print(f"✅ Requisições bem-sucedidas: {successful_requests}")
        print(f"❌ Requisições falharam: {failed_requests}")
        print(f"📊 Tempo total: {total_time:.2f}s")
        print(f"📊 Requests por segundo: {len(results)/total_time:.2f}")
        
        if response_times:
            print(f"⏱️  Tempo médio de resposta: {statistics.mean(response_times):.3f}s")
            print(f"⏱️  Tempo mínimo: {min(response_times):.3f}s")
            print(f"⏱️  Tempo máximo: {max(response_times):.3f}s")
            print(f"⏱️  Mediana: {statistics.median(response_times):.3f}s")
            
        return {
            'total_requests': len(results),
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'total_time': total_time,
            'rps': len(results)/total_time,
            'avg_response_time': statistics.mean(response_times) if response_times else 0,
            'response_times': response_times
        }
    
    def test_memory_usage(self):
        """Testa uso de memória (se psutil estiver disponível)"""
        try:
            import psutil
            import os
            
            print(f"\n💾 ANÁLISE DE MEMÓRIA")
            print("-" * 50)
            
            # Memória do sistema
            memory = psutil.virtual_memory()
            print(f"💾 Memória total: {memory.total / (1024**3):.2f} GB")
            print(f"💾 Memória usada: {memory.used / (1024**3):.2f} GB ({memory.percent:.1f}%)")
            print(f"💾 Memória disponível: {memory.available / (1024**3):.2f} GB")
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"🖥️  CPU utilização: {cpu_percent:.1f}%")
            
        except ImportError:
            print("\n💾 ANÁLISE DE MEMÓRIA")
            print("-" * 50)
            print("⚠️  psutil não instalado - instale com: pip install psutil")
    
    def run_full_test(self):
        """Executa teste completo"""
        print("🧪 TESTE DE CARGA E PERFORMANCE - SISTEMA PULSE")
        print("=" * 60)
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        # URLs para testar
        urls = [
            f"{self.base_url}/consultorio/",
            f"{self.base_url}/consultorio/agenda/",
            f"{self.base_url}/consultorio/pacientes/",
            f"{self.base_url}/consultorio/financeiro/",
            f"{self.base_url}/admin/",
        ]
        
        # Teste básico de conectividade
        print("\n🔍 TESTE BÁSICO DE CONECTIVIDADE")
        print("-" * 50)
        
        for url in urls:
            result = self.test_single_request(url)
            if result['success']:
                print(f"✅ {url} - {result['status_code']} - {result['response_time']:.3f}s")
            else:
                print(f"❌ {url} - Erro: {result.get('error', 'Falha na requisição')}")
        
        # Teste de carga com diferentes níveis
        load_tests = [
            (1, "1 usuário (baseline)"),
            (3, "3 usuários simultâneos"),
            (5, "5 usuários simultâneos"),
            (10, "10 usuários simultâneos (stress test)")
        ]
        
        results = []
        for concurrent_users, description in load_tests:
            print(f"\n🔄 {description.upper()}")
            result = self.test_concurrent_requests(urls, concurrent_users)
            results.append((concurrent_users, result))
            
            # Pausa entre testes
            if concurrent_users < 10:
                time.sleep(2)
        
        # Análise de memória
        self.test_memory_usage()
        
        # Relatório final
        self.generate_performance_report(results)
        
        return results
    
    def generate_performance_report(self, results):
        """Gera relatório de performance"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO DE PERFORMANCE")
        print("=" * 60)
        
        print("\n📈 RESUMO POR NÚMERO DE USUÁRIOS:")
        print("-" * 50)
        
        for users, result in results:
            success_rate = (result['successful_requests'] / result['total_requests']) * 100
            print(f"👥 {users:2d} usuários: {result['rps']:6.2f} req/s | "
                  f"{result['avg_response_time']:6.3f}s avg | "
                  f"{success_rate:5.1f}% sucesso")
        
        # Recomendações
        print("\n💡 RECOMENDAÇÕES:")
        print("-" * 50)
        
        best_result = max(results, key=lambda x: x[1]['rps'])
        worst_result = min(results, key=lambda x: x[1]['rps'])
        
        print(f"🏆 Melhor performance: {best_result[0]} usuários ({best_result[1]['rps']:.2f} req/s)")
        
        if any(r[1]['failed_requests'] > 0 for r in results):
            print("⚠️  Algumas requisições falharam - verificar logs do servidor")
        else:
            print("✅ Todas as requisições foram bem-sucedidas")
            
        # Análise de tempo de resposta
        all_response_times = []
        for _, result in results:
            all_response_times.extend(result['response_times'])
            
        if all_response_times:
            avg_all = statistics.mean(all_response_times)
            if avg_all < 0.1:
                print("🚀 Tempos de resposta excelentes (< 100ms)")
            elif avg_all < 0.5:
                print("✅ Tempos de resposta bons (< 500ms)")
            elif avg_all < 1.0:
                print("⚠️  Tempos de resposta aceitáveis (< 1s)")
            else:
                print("❌ Tempos de resposta lentos (> 1s) - otimização necessária")

def main():
    """Função principal"""
    tester = PulseLoadTester()
    
    try:
        results = tester.run_full_test()
        
        # Determinar se passou no teste
        all_successful = all(r[1]['failed_requests'] == 0 for r in results)
        good_performance = all(r[1]['avg_response_time'] < 2.0 for r in results)
        
        if all_successful and good_performance:
            print("\n🎉 SISTEMA APROVADO NO TESTE DE CARGA!")
            print("✅ Performance excelente e sem erros")
            exit(0)
        else:
            print("\n⚠️  Sistema precisa de otimizações")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ Erro durante teste de carga: {e}")
        exit(1)

if __name__ == "__main__":
    main()
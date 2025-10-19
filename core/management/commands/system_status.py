"""
Comando para monitoramento do sistema
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.contrib.auth import get_user_model
from core.models import Profissional, Servico, Agendamento
import os
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Mostra status do sistema Pulse'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Mostra informações detalhadas'
        )

    def handle(self, *args, **options):
        detailed = options['detailed']
        
        self.stdout.write(self.style.SUCCESS('=== STATUS DO SISTEMA PULSE ===\n'))
        
        # 1. Informações básicas
        self.stdout.write('📊 INFORMAÇÕES GERAIS:')
        self.stdout.write(f'  Data/Hora: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        self.stdout.write(f'  Ambiente: {"Desenvolvimento" if settings.DEBUG else "Produção"}')
        self.stdout.write(f'  Diretório: {settings.BASE_DIR}')
        
        # 2. Banco de dados
        self.stdout.write('\n💾 BANCO DE DADOS:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write('  Status: ✓ Conectado')
            
            # Estatísticas de dados
            users_count = User.objects.count()
            profissionais_count = Profissional.objects.count()
            servicos_count = Servico.objects.count()
            agendamentos_count = Agendamento.objects.count()
            
            self.stdout.write(f'  Usuários: {users_count}')
            self.stdout.write(f'  Profissionais: {profissionais_count}')
            self.stdout.write(f'  Serviços: {servicos_count}')
            self.stdout.write(f'  Agendamentos: {agendamentos_count}')
            
        except Exception as e:
            self.stdout.write(f'  Status: ❌ Erro - {e}')
        
        # 3. Sistema de arquivos
        self.stdout.write('\n📁 SISTEMA DE ARQUIVOS:')
        
        # Verificar diretórios importantes
        directories = [
            ('Logs', settings.BASE_DIR / 'logs'),
            ('Static', getattr(settings, 'STATIC_ROOT', 'Não configurado')),
            ('Media', getattr(settings, 'MEDIA_ROOT', 'Não configurado')),
        ]
        
        for name, path in directories:
            if path and path != 'Não configurado':
                if os.path.exists(path):
                    if os.path.isdir(path):
                        files_count = len(os.listdir(path))
                        self.stdout.write(f'  {name}: ✓ Existe ({files_count} itens)')
                    else:
                        self.stdout.write(f'  {name}: ⚠️  Não é um diretório')
                else:
                    self.stdout.write(f'  {name}: ❌ Não existe')
            else:
                self.stdout.write(f'  {name}: ⚠️  {path}')
        
        # 4. Performance do sistema (se psutil estiver disponível)
        try:
            import psutil
            
            self.stdout.write('\n⚡ PERFORMANCE:')
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            self.stdout.write(f'  CPU: {cpu_percent}%')
            
            # Memória
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB
            self.stdout.write(f'  Memória: {memory_percent}% ({memory_used:.1f}GB / {memory_total:.1f}GB)')
            
            # Disco
            disk = psutil.disk_usage(str(settings.BASE_DIR))
            disk_percent = (disk.used / disk.total) * 100
            disk_free = disk.free / (1024**3)  # GB
            self.stdout.write(f'  Disco: {disk_percent:.1f}% usado ({disk_free:.1f}GB livres)')
            
        except ImportError:
            self.stdout.write('\n⚡ PERFORMANCE: psutil não instalado')
        except Exception as e:
            self.stdout.write(f'\n⚡ PERFORMANCE: Erro - {e}')
        
        # 5. Logs recentes (se detailed)
        if detailed:
            self.stdout.write('\n📋 LOGS RECENTES:')
            logs_dir = settings.BASE_DIR / 'logs'
            
            if logs_dir.exists():
                log_files = list(logs_dir.glob('*.log'))
                if log_files:
                    # Mostrar apenas os 3 logs mais recentes
                    recent_logs = sorted(log_files, key=lambda x: x.stat().st_mtime, reverse=True)[:3]
                    
                    for log_file in recent_logs:
                        try:
                            size = log_file.stat().st_size / 1024  # KB
                            modified = datetime.datetime.fromtimestamp(log_file.stat().st_mtime)
                            self.stdout.write(f'  {log_file.name}: {size:.1f}KB ({modified.strftime("%d/%m %H:%M")})')
                        except Exception as e:
                            self.stdout.write(f'  {log_file.name}: Erro ao ler - {e}')
                else:
                    self.stdout.write('  Nenhum arquivo de log encontrado')
            else:
                self.stdout.write('  Diretório de logs não existe')
        
        # 6. Agendamentos de hoje
        self.stdout.write('\n📅 AGENDAMENTOS HOJE:')
        hoje = datetime.date.today()
        agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje)
        
        if agendamentos_hoje.exists():
            self.stdout.write(f'  Total: {agendamentos_hoje.count()}')
            
            if detailed:
                for agendamento in agendamentos_hoje.order_by('data_hora')[:5]:
                    status_icon = '✓' if agendamento.status == 'confirmado' else '⏳'
                    self.stdout.write(
                        f'  {status_icon} {agendamento.data_hora.strftime("%H:%M")} - '
                        f'{agendamento.cliente.first_name} '
                        f'({agendamento.servico.nome})'
                    )
                
                if agendamentos_hoje.count() > 5:
                    self.stdout.write(f'  ... e mais {agendamentos_hoje.count() - 5}')
        else:
            self.stdout.write('  Nenhum agendamento para hoje')
        
        self.stdout.write(f'\n{self.style.SUCCESS("=== FIM DO STATUS ===")}')
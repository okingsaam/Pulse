"""
Script de manutenção automatizada do sistema Pulse
Execute: python manage.py daily_maintenance
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connection
import datetime
import os

class Command(BaseCommand):
    help = 'Executa manutenção diária automatizada do sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Inclui backup no processo de manutenção'
        )
        parser.add_argument(
            '--cleanup-days',
            type=int,
            default=7,
            help='Dias de logs para manter (padrão: 7)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔧 INICIANDO MANUTENÇÃO DIÁRIA DO SISTEMA PULSE')
        )
        
        start_time = datetime.datetime.now()
        
        # 1. Verificar saúde do sistema
        self.stdout.write('\n1️⃣ Verificando saúde do sistema...')
        try:
            # Testar conexão com banco
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write('   ✓ Banco de dados: OK')
            
            # Verificar diretórios críticos
            logs_dir = settings.BASE_DIR / 'logs'
            if not logs_dir.exists():
                logs_dir.mkdir(parents=True)
                self.stdout.write('   ✓ Diretório de logs criado')
            else:
                self.stdout.write('   ✓ Diretório de logs: OK')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Erro na verificação: {e}')
            )
            return
        
        # 2. Limpeza de logs antigos
        self.stdout.write('\n2️⃣ Limpando logs antigos...')
        try:
            call_command('cleanup_logs', days=options['cleanup_days'])
            self.stdout.write('   ✓ Limpeza de logs concluída')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'   ⚠️ Erro na limpeza de logs: {e}')
            )
        
        # 3. Otimização do banco de dados
        self.stdout.write('\n3️⃣ Otimizando banco de dados...')
        try:
            # SQLite - VACUUM para otimizar
            if 'sqlite' in settings.DATABASES['default']['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("VACUUM")
                self.stdout.write('   ✓ VACUUM SQLite executado')
            else:
                self.stdout.write('   ℹ️ Otimização não implementada para este banco')
                
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'   ⚠️ Erro na otimização: {e}')
            )
        
        # 4. Verificar integridade dos dados
        self.stdout.write('\n4️⃣ Verificando integridade dos dados...')
        try:
            call_command('check')
            self.stdout.write('   ✓ Verificações do Django: OK')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'   ⚠️ Problemas encontrados: {e}')
            )
        
        # 5. Backup (se solicitado)
        if options['backup']:
            self.stdout.write('\n5️⃣ Criando backup...')
            try:
                timestamp = datetime.datetime.now().strftime('%Y%m%d')
                backup_dir = f'backups/maintenance_{timestamp}'
                call_command('backup_system', output_dir='backups')
                self.stdout.write('   ✓ Backup criado com sucesso')
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'   ⚠️ Erro no backup: {e}')
                )
        
        # 6. Relatório final
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.stdout.write('\n📊 RELATÓRIO DA MANUTENÇÃO:')
        self.stdout.write(f'   Início: {start_time.strftime("%d/%m/%Y %H:%M:%S")}')
        self.stdout.write(f'   Fim: {end_time.strftime("%d/%m/%Y %H:%M:%S")}')
        self.stdout.write(f'   Duração: {duration:.2f} segundos')
        
        # Log da manutenção
        try:
            log_file = settings.BASE_DIR / 'logs' / 'maintenance.log'
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f'{end_time.isoformat()}: Manutenção concluída em {duration:.2f}s\n')
        except Exception:
            pass  # Não falhar se não conseguir logar
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ MANUTENÇÃO CONCLUÍDA COM SUCESSO!')
        )
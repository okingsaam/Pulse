"""
Comando para fazer backup do banco de dados
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import django
import os
import datetime
import shutil

class Command(BaseCommand):
    help = 'Faz backup completo do sistema Pulse'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='backups',
            help='Diretório para salvar os backups'
        )

    def handle(self, *args, **options):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(options['output_dir'], f'pulse_backup_{timestamp}')
        
        # Criar diretório de backup
        os.makedirs(backup_dir, exist_ok=True)
        
        self.stdout.write('Iniciando backup do sistema Pulse...')
        
        try:
            # 1. Backup do banco de dados
            db_backup_file = os.path.join(backup_dir, 'database.json')
            with open(db_backup_file, 'w') as f:
                call_command('dumpdata', stdout=f, indent=2)
            self.stdout.write(f'✓ Backup do banco salvo em: {db_backup_file}')
            
            # 2. Backup dos arquivos de mídia (se existirem)
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            if media_root and os.path.exists(media_root):
                media_backup_dir = os.path.join(backup_dir, 'media')
                shutil.copytree(media_root, media_backup_dir)
                self.stdout.write(f'✓ Backup da mídia salvo em: {media_backup_dir}')
            
            # 3. Backup dos arquivos estáticos
            static_root = getattr(settings, 'STATIC_ROOT', None)
            if static_root and os.path.exists(static_root):
                static_backup_dir = os.path.join(backup_dir, 'static')
                shutil.copytree(static_root, static_backup_dir)
                self.stdout.write(f'✓ Backup dos estáticos salvo em: {static_backup_dir}')
            
            # 4. Backup dos logs
            logs_dir = settings.BASE_DIR / 'logs'
            if logs_dir.exists():
                logs_backup_dir = os.path.join(backup_dir, 'logs')
                shutil.copytree(logs_dir, logs_backup_dir)
                self.stdout.write(f'✓ Backup dos logs salvo em: {logs_backup_dir}')
            
            # 5. Criar arquivo de informações do backup
            info_file = os.path.join(backup_dir, 'backup_info.txt')
            with open(info_file, 'w') as f:
                f.write(f'Backup do Sistema Pulse\n')
                f.write(f'Data: {datetime.datetime.now()}\n')
                f.write(f'Versão Django: {django.get_version()}\n')
                f.write(f'Ambiente: {settings.DEBUG and "Desenvolvimento" or "Produção"}\n')
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Backup completo criado em: {backup_dir}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro durante o backup: {e}')
            )
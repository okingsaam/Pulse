"""
Comando para restaurar backup do sistema
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os
import json
import shutil

class Command(BaseCommand):
    help = 'Restaura backup do sistema Pulse'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_dir',
            type=str,
            help='Diretório do backup a ser restaurado'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a restauração sem confirmação'
        )

    def handle(self, *args, **options):
        backup_dir = options['backup_dir']
        
        if not os.path.exists(backup_dir):
            self.stdout.write(
                self.style.ERROR(f'Diretório de backup não encontrado: {backup_dir}')
            )
            return
        
        # Verificar se existe backup válido
        db_backup_file = os.path.join(backup_dir, 'database.json')
        if not os.path.exists(db_backup_file):
            self.stdout.write(
                self.style.ERROR('Arquivo de backup do banco não encontrado!')
            )
            return
        
        if not options['force']:
            confirm = input('⚠️  ATENÇÃO: Esta operação irá substituir todos os dados atuais. Continuar? (s/N): ')
            if confirm.lower() != 's':
                self.stdout.write('Operação cancelada.')
                return
        
        self.stdout.write('Iniciando restauração do backup...')
        
        try:
            # 1. Limpar banco atual
            self.stdout.write('Limpando banco de dados atual...')
            call_command('flush', '--noinput')
            
            # 2. Restaurar dados do banco
            self.stdout.write('Restaurando dados do banco...')
            call_command('loaddata', db_backup_file)
            self.stdout.write('✓ Banco de dados restaurado')
            
            # 3. Restaurar arquivos de mídia
            media_backup_dir = os.path.join(backup_dir, 'media')
            if os.path.exists(media_backup_dir):
                media_root = getattr(settings, 'MEDIA_ROOT', None)
                if media_root:
                    if os.path.exists(media_root):
                        shutil.rmtree(media_root)
                    shutil.copytree(media_backup_dir, media_root)
                    self.stdout.write('✓ Arquivos de mídia restaurados')
            
            # 4. Restaurar logs
            logs_backup_dir = os.path.join(backup_dir, 'logs')
            if os.path.exists(logs_backup_dir):
                logs_dir = settings.BASE_DIR / 'logs'
                if logs_dir.exists():
                    shutil.rmtree(logs_dir)
                shutil.copytree(logs_backup_dir, logs_dir)
                self.stdout.write('✓ Logs restaurados')
            
            # 5. Mostrar informações do backup
            info_file = os.path.join(backup_dir, 'backup_info.txt')
            if os.path.exists(info_file):
                self.stdout.write('\n📋 Informações do backup:')
                with open(info_file, 'r') as f:
                    self.stdout.write(f.read())
            
            self.stdout.write(
                self.style.SUCCESS('✓ Restauração concluída com sucesso!')
            )
            self.stdout.write(
                self.style.WARNING('🔄 Execute as migrações se necessário: python manage.py migrate')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro durante a restauração: {e}')
            )
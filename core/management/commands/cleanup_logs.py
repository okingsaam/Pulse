"""
Comando para limpeza de logs antigos
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os
import datetime
import glob

class Command(BaseCommand):
    help = 'Remove logs antigos do sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Dias de logs para manter (padrão: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra quais arquivos seriam removidos sem remover'
        )

    def handle(self, *args, **options):
        days_to_keep = options['days']
        dry_run = options['dry_run']
        
        logs_dir = settings.BASE_DIR / 'logs'
        
        if not logs_dir.exists():
            self.stdout.write('Diretório de logs não encontrado.')
            return
        
        # Calcular data limite
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_to_keep)
        
        self.stdout.write(f'Procurando logs anteriores a {cutoff_date.strftime("%d/%m/%Y")}...')
        
        # Buscar todos os arquivos de log
        log_files = glob.glob(str(logs_dir / '*.log*'))
        
        removed_count = 0
        total_size = 0
        
        for log_file in log_files:
            try:
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
                
                if file_time < cutoff_date:
                    file_size = os.path.getsize(log_file)
                    total_size += file_size
                    
                    if dry_run:
                        self.stdout.write(f'[DRY RUN] Removeria: {log_file} ({file_size} bytes)')
                    else:
                        os.remove(log_file)
                        self.stdout.write(f'Removido: {log_file}')
                    
                    removed_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Erro ao processar {log_file}: {e}')
                )
        
        if removed_count == 0:
            self.stdout.write('Nenhum log antigo encontrado.')
        else:
            action = 'seriam removidos' if dry_run else 'removidos'
            size_mb = total_size / (1024 * 1024)
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ {removed_count} arquivos de log {action} '
                    f'({size_mb:.2f} MB liberados)'
                )
            )
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        'Execute sem --dry-run para remover os arquivos'
                    )
                )
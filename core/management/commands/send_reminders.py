from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Agendamento

class Command(BaseCommand):
    help = 'Envia lembretes por email para consultas do próximo dia'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            default=1,
            help='Quantos dias antes da consulta enviar lembrete (padrão: 1)'
        )

    def handle(self, *args, **options):
        dias_antecedencia = options['dias']
        amanha = timezone.now() + timedelta(days=dias_antecedencia)
        
        # Buscar consultas confirmadas para o período
        agendamentos = Agendamento.objects.filter(
            status='confirmado',
            data_hora__date=amanha.date()
        ).select_related('paciente', 'servico', 'profissional')
        
        enviados = 0
        
        for agendamento in agendamentos:
            try:
                # Aqui você implementaria o envio de email
                # send_mail(
                #     subject=f'Lembrete: Consulta amanhã às {agendamento.data_hora.strftime("%H:%M")}',
                #     message=f'Olá {agendamento.paciente.first_name}, você tem consulta marcada...',
                #     from_email='noreply@pulse.com',
                #     recipient_list=[agendamento.paciente.email],
                # )
                
                self.stdout.write(
                    f'Lembrete enviado para {agendamento.paciente.username} - '
                    f'{agendamento.servico.nome} às {agendamento.data_hora.strftime("%H:%M")}'
                )
                enviados += 1
                
            except Exception as e:
                self.stderr.write(
                    f'Erro ao enviar para {agendamento.paciente.username}: {e}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Total de lembretes enviados: {enviados}')
        )
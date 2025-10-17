from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Profissional, Servico
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria dados de exemplo para o sistema'

    def handle(self, *args, **options):
        # Criar usuário admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@pulse.com',
                password='admin123',
                role='admin'
            )
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            self.stdout.write(f'Admin criado: admin/admin123')

        # Criar profissionais
        profissionais_data = [
            {'nome': 'Dr. João Silva', 'especialidade': 'Cardiologia'},
            {'nome': 'Dra. Maria Santos', 'especialidade': 'Dermatologia'},
            {'nome': 'Dr. Carlos Lima', 'especialidade': 'Ortopedia'},
            {'nome': 'Dra. Ana Costa', 'especialidade': 'Ginecologia'},
        ]
        
        for prof_data in profissionais_data:
            prof, created = Profissional.objects.get_or_create(**prof_data)
            if created:
                self.stdout.write(f'Profissional criado: {prof.nome}')

        # Criar serviços
        servicos_data = [
            {'nome': 'Consulta Cardiológica', 'descricao': 'Consulta com cardiologista', 'duracao': timedelta(hours=1), 'preco': 200.00},
            {'nome': 'Consulta Dermatológica', 'descricao': 'Consulta com dermatologista', 'duracao': timedelta(minutes=45), 'preco': 180.00},
            {'nome': 'Consulta Ortopédica', 'descricao': 'Consulta com ortopedista', 'duracao': timedelta(hours=1), 'preco': 220.00},
            {'nome': 'Consulta Ginecológica', 'descricao': 'Consulta com ginecologista', 'duracao': timedelta(hours=1), 'preco': 190.00},
        ]
        
        profissionais = Profissional.objects.all()
        for i, serv_data in enumerate(servicos_data):
            serv_data['profissional'] = profissionais[i]
            servico, created = Servico.objects.get_or_create(
                nome=serv_data['nome'],
                defaults=serv_data
            )
            if created:
                self.stdout.write(f'Serviço criado: {servico.nome}')

        self.stdout.write(self.style.SUCCESS('Dados de exemplo criados com sucesso!'))
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import Paciente, Profissional, Agendamento, Consulta, Servico
import random

class Command(BaseCommand):
    help = 'Cria dados de exemplo para o sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Remove dados existentes antes de criar novos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('🗑️  Removendo dados existentes...')
            Consulta.objects.all().delete()
            Agendamento.objects.all().delete()
            Paciente.objects.all().delete()
            Profissional.objects.all().delete()
            Servico.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('👨‍💼 Criando usuários...')
        self.create_users()
        
        self.stdout.write('👨‍⚕️ Criando profissionais...')
        self.create_profissionais()
        
        self.stdout.write('🏥 Criando serviços...')
        self.create_servicos()
        
        self.stdout.write('👥 Criando pacientes...')
        self.create_pacientes()
        
        self.stdout.write('📅 Criando agendamentos...')
        self.create_agendamentos()
        
        self.stdout.write('💊 Criando consultas...')
        self.create_consultas()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Dados de exemplo criados com sucesso!')
        )

    def create_users(self):
        """Criar usuários para os profissionais"""
        users_data = [
            {'username': 'dr.silva', 'first_name': 'João', 'last_name': 'Silva', 'email': 'joao.silva@pulse.com'},
            {'username': 'dra.santos', 'first_name': 'Maria', 'last_name': 'Santos', 'email': 'maria.santos@pulse.com'},
            {'username': 'dr.oliveira', 'first_name': 'Carlos', 'last_name': 'Oliveira', 'email': 'carlos.oliveira@pulse.com'},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                    'is_staff': True,
                }
            )
            if created:
                user.set_password('pulse123')
                user.save()
                self.stdout.write(f'  ✅ Usuário {user.username} criado')

    def create_profissionais(self):
        """Criar profissionais"""
        users = User.objects.filter(is_superuser=False)
        especialidades = ['Clínica Geral', 'Cardiologia', 'Dermatologia']
        crms = ['12345-SP', '67890-SP', '54321-SP']
        
        for i, user in enumerate(users):
            profissional, created = Profissional.objects.get_or_create(
                usuario=user,
                defaults={
                    'crm': crms[i],
                    'especialidade': especialidades[i],
                    'telefone': f'(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}',
                    'email': user.email,
                    'ativo': True,
                }
            )
            if created:
                self.stdout.write(f'  ✅ Profissional {profissional.usuario.get_full_name()} criado')

    def create_servicos(self):
        """Criar serviços"""
        servicos_data = [
            {'nome': 'Consulta Clínica Geral', 'descricao': 'Consulta médica geral', 'valor': 150.00},
            {'nome': 'Consulta Cardiológica', 'descricao': 'Consulta especializada em cardiologia', 'valor': 200.00},
            {'nome': 'Consulta Dermatológica', 'descricao': 'Consulta especializada em dermatologia', 'valor': 180.00},
            {'nome': 'Exame de Rotina', 'descricao': 'Exames laboratoriais básicos', 'valor': 80.00},
            {'nome': 'Eletrocardiograma', 'descricao': 'ECG para avaliação cardíaca', 'valor': 120.00},
        ]
        
        for servico_data in servicos_data:
            servico, created = Servico.objects.get_or_create(
                nome=servico_data['nome'],
                defaults=servico_data
            )
            if created:
                self.stdout.write(f'  ✅ Serviço {servico.nome} criado')

    def create_pacientes(self):
        """Criar pacientes"""
        nomes = [
            'Ana Silva Costa', 'Pedro Santos Oliveira', 'Maria José Ferreira',
            'João Carlos Pereira', 'Fernanda Lima Rocha', 'Ricardo Alves Mendes',
            'Juliana Rodrigues Sousa', 'Gabriel Martins Cruz', 'Larissa Cunha Dias',
            'Bruno Barbosa Reis', 'Camila Teixeira Moura', 'Diego Nascimento Viana',
            'Beatriz Cardoso Freitas', 'Lucas Monteiro Araújo', 'Isabela Correia Pinto',
        ]
        
        cpfs = [
            '123.456.789-10', '234.567.891-23', '345.678.912-34',
            '456.789.123-45', '567.891.234-56', '678.912.345-67',
            '789.123.456-78', '891.234.567-89', '912.345.678-91',
            '123.345.567-89', '234.456.678-90', '345.567.789-01',
            '456.678.890-12', '567.789.901-23', '678.890.012-34',
        ]
        
        for i, nome in enumerate(nomes):
            data_nascimento = datetime.now().date() - timedelta(days=random.randint(18*365, 80*365))
            
            paciente, created = Paciente.objects.get_or_create(
                cpf=cpfs[i],
                defaults={
                    'nome': nome,
                    'data_nascimento': data_nascimento,
                    'sexo': random.choice(['M', 'F']),
                    'telefone': f'(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}',
                    'email': f'{nome.lower().replace(" ", ".")}@email.com',
                    'endereco': f'Rua {random.choice(["das Flores", "dos Jardins", "da Paz"])}, {random.randint(100,999)}',
                    'ativo': True,
                }
            )
            if created:
                self.stdout.write(f'  ✅ Paciente {paciente.nome} criado')

    def create_agendamentos(self):
        """Criar agendamentos"""
        pacientes = list(Paciente.objects.all())
        profissionais = list(Profissional.objects.all())
        servicos = list(Servico.objects.all())
        
        if not (pacientes and profissionais and servicos):
            self.stdout.write('⚠️  Não há dados suficientes para criar agendamentos')
            return
        
        # Agendamentos passados (últimos 30 dias)
        for _ in range(20):
            data_passada = timezone.now() - timedelta(days=random.randint(1, 30))
            self.create_agendamento(
                random.choice(pacientes),
                random.choice(profissionais),
                random.choice(servicos),
                data_passada,
                random.choice(['realizado', 'cancelado', 'faltou'])
            )
        
        # Agendamentos futuros
        for _ in range(15):
            data_futura = timezone.now() + timedelta(days=random.randint(1, 60))
            self.create_agendamento(
                random.choice(pacientes),
                random.choice(profissionais),
                random.choice(servicos),
                data_futura,
                random.choice(['agendado', 'confirmado'])
            )

    def create_agendamento(self, paciente, profissional, servico, data_hora, status):
        """Criar um agendamento específico"""
        agendamento, created = Agendamento.objects.get_or_create(
            paciente=paciente,
            profissional=profissional,
            data_hora=data_hora,
            defaults={
                'servico': servico,
                'status': status,
                'observacoes': 'Agendamento criado automaticamente',
            }
        )
        if created:
            self.stdout.write(f'  ✅ Agendamento para {paciente.nome} criado')

    def create_consultas(self):
        """Criar consultas para agendamentos realizados"""
        agendamentos_realizados = Agendamento.objects.filter(status='realizado')
        
        sintomas_exemplos = [
            'Dor de cabeça frequente',
            'Dor no peito ao esforço',
            'Manchas na pele',
            'Fadiga e cansaço',
            'Dor abdominal',
            'Tosse persistente',
            'Dor nas articulações',
        ]
        
        diagnosticos_exemplos = [
            'Cefaleia tensional',
            'Angina estável',
            'Dermatite de contato',
            'Anemia ferropriva',
            'Gastrite',
            'Bronquite',
            'Artrite',
        ]
        
        tratamentos_exemplos = [
            'Analgésicos e repouso',
            'Betabloqueadores e mudança de hábitos',
            'Corticosteroides tópicos',
            'Suplementação de ferro',
            'Inibidores da bomba de prótons',
            'Broncodilatadores',
            'Anti-inflamatórios não esteroidais',
        ]
        
        for agendamento in agendamentos_realizados:
            consulta, created = Consulta.objects.get_or_create(
                agendamento=agendamento,
                defaults={
                    'sintomas': random.choice(sintomas_exemplos),
                    'diagnostico': random.choice(diagnosticos_exemplos),
                    'tratamento': random.choice(tratamentos_exemplos),
                    'valor': agendamento.servico.valor if agendamento.servico else 150.00,
                    'pago': random.choice([True, False]),
                    'observacoes': 'Consulta registrada automaticamente',
                }
            )
            if created:
                self.stdout.write(f'  ✅ Consulta para {agendamento.paciente.nome} criada')
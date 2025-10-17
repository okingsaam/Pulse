from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profissional, Servico, Agendamento

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = ['id', 'nome', 'especialidade']

class ServicoSerializer(serializers.ModelSerializer):
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True)
    
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'duracao', 'preco', 'profissional', 'profissional_nome']

class AgendamentoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.username', read_only=True)
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    profissional_nome = serializers.CharField(source='profissional.nome', read_only=True)
    
    class Meta:
        model = Agendamento
        fields = [
            'id', 'paciente', 'paciente_nome', 'servico', 'servico_nome', 
            'profissional', 'profissional_nome', 'data_hora', 'status', 'observacoes'
        ]
        read_only_fields = ['paciente']
"""
FORMS.PY - Formulários do Sistema Pulse
=======================================
Este arquivo define os formulários HTML que o usuário preenche.
Cada formulário valida os dados e gera campos HTML automaticamente.

ESTRUTURA:
1. Formulário de cadastro de usuário
2. Formulários para os modelos (Agendamento, Profissional, Serviço)
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Agendamento, Profissional, Servico

# Pega o modelo User atual (nosso User customizado)
User = get_user_model()

# ==========================================
# FORMULÁRIO DE CADASTRO DE USUÁRIO
# ==========================================
class CustomUserCreationForm(UserCreationForm):
    """
    Formulário de cadastro que estende o UserCreationForm padrão.
    Adiciona campos email e telefone.
    """
    # Campos extras além de username/password
    email = forms.EmailField(
        required=True,
        help_text="Email válido é obrigatório"
    )
    phone = forms.CharField(
        max_length=20, 
        required=False,
        label="Telefone",
        help_text="Opcional - para contato"
    )
    
    class Meta:
        model = User
        # Campos que aparecerão no formulário
        fields = ("username", "email", "phone", "password1", "password2")
        # password1 = senha, password2 = confirmação

    def save(self, commit=True):
        """
        Método que salva o usuário no banco.
        Chamado quando form.save() é executado.
        """
        # Cria o usuário mas não salva ainda
        user = super().save(commit=False)
        
        # Define os campos extras
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.role = 'paciente'  # Todo novo usuário é paciente por padrão
        
        # Se commit=True, salva no banco
        if commit:
            user.save()
        return user

# ==========================================
# FORMULÁRIO DE AGENDAMENTO
# ==========================================
class AgendamentoForm(forms.ModelForm):
    """
    Formulário para criar/editar agendamentos.
    Baseado no modelo Agendamento.
    """
    class Meta:
        model = Agendamento
        # Campos que aparecerão no formulário
        fields = ['servico', 'profissional', 'data_hora', 'observacoes']
        # 'paciente' não aparece porque é definido automaticamente
        
        # Customização dos widgets (como os campos aparecem)
        widgets = {
            'data_hora': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',  # Campo de data/hora do HTML5
                    'class': 'form-control'
                }
            ),
            'observacoes': forms.Textarea(
                attrs={
                    'rows': 3,  # 3 linhas de altura
                    'class': 'form-control',
                    'placeholder': 'Informações adicionais (opcional)'
                }
            ),
        }
        
        # Labels personalizados
        labels = {
            'servico': 'Tipo de Consulta',
            'profissional': 'Médico',
            'data_hora': 'Data e Hora',
            'observacoes': 'Observações'
        }

# ==========================================
# FORMULÁRIO DE PROFISSIONAL
# ==========================================
class ProfissionalForm(forms.ModelForm):
    """
    Formulário para cadastrar/editar médicos.
    Usado apenas por administradores.
    """
    class Meta:
        model = Profissional
        fields = ['nome', 'especialidade']
        
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Dr. João Silva'
                }
            ),
            'especialidade': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Cardiologia'
                }
            ),
        }

# ==========================================
# FORMULÁRIO DE SERVIÇO
# ==========================================
class ServicoForm(forms.ModelForm):
    """
    Formulário para cadastrar/editar serviços.
    Usado apenas por administradores.
    """
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'duracao', 'preco', 'profissional']
        
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Consulta Cardiológica'
                }
            ),
            'descricao': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-control',
                    'placeholder': 'Descreva o serviço...'
                }
            ),
            'duracao': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: 01:00:00 (1 hora)'
                }
            ),
            'preco': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',  # Permite centavos
                    'placeholder': 'Ex: 200.00'
                }
            ),
            'profissional': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }
        
        labels = {
            'nome': 'Nome do Serviço',
            'descricao': 'Descrição',
            'duracao': 'Duração (HH:MM:SS)',
            'preco': 'Preço (R$)',
            'profissional': 'Profissional Responsável'
        }

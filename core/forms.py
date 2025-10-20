from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Paciente, Agendamento, Profissional, Servico, Consulta

class PacienteForm(forms.ModelForm):
    """Formulário para cadastro e edição de pacientes"""
    
    class Meta:
        model = Paciente
        fields = [
            'nome', 'cpf', 'rg', 'data_nascimento', 'sexo',
            'telefone', 'email', 'endereco', 'observacoes', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do paciente'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'maxlength': '14'
            }),
            'rg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do RG'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre o paciente'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_cpf(self):
        """Validação customizada do CPF"""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf_numbers = ''.join(filter(str.isdigit, cpf))
            
            # Verifica se tem 11 dígitos
            if len(cpf_numbers) != 11:
                raise forms.ValidationError("CPF deve ter 11 dígitos")
            
            # Adiciona formatação se necessário
            if len(cpf) == 11 and cpf.isdigit():
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                
        return cpf
    
    def clean_telefone(self):
        """Validação do telefone"""
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remove caracteres não numéricos
            phone_numbers = ''.join(filter(str.isdigit, telefone))
            
            # Verifica se tem pelo menos 10 dígitos
            if len(phone_numbers) < 10:
                raise forms.ValidationError("Telefone deve ter pelo menos 10 dígitos")
                
        return telefone

class AgendamentoForm(forms.ModelForm):
    """Formulário para agendamentos"""
    
    class Meta:
        model = Agendamento
        fields = [
            'paciente', 'profissional', 'servico', 'data_hora',
            'status', 'observacoes'
        ]
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'profissional': forms.Select(attrs={
                'class': 'form-control'
            }),
            'servico': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_hora': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre o agendamento'
            })
        }
    
    def clean_data_hora(self):
        """Validação da data e hora"""
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        data_hora = self.cleaned_data.get('data_hora')
        if data_hora:
            # Não permitir agendamentos no passado
            if data_hora < timezone.now():
                raise forms.ValidationError("Não é possível agendar para uma data no passado")
            
            # Não permitir agendamentos muito no futuro (1 ano)
            if data_hora > timezone.now() + timedelta(days=365):
                raise forms.ValidationError("Não é possível agendar com mais de 1 ano de antecedência")
                
        return data_hora

class ProfissionalForm(forms.ModelForm):
    """Formulário para profissionais"""
    
    class Meta:
        model = Profissional
        fields = [
            'usuario', 'crm', 'especialidade', 'telefone',
            'email', 'ativo'
        ]
        widgets = {
            'usuario': forms.Select(attrs={
                'class': 'form-control'
            }),
            'crm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do CRM'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especialidade médica'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

class ServicoForm(forms.ModelForm):
    """Formulário para serviços"""
    
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'valor', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do serviço'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do serviço'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_valor(self):
        """Validação do valor"""
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor < 0:
            raise forms.ValidationError("O valor não pode ser negativo")
        return valor

class ConsultaForm(forms.ModelForm):
    """Formulário para consultas"""
    
    class Meta:
        model = Consulta
        fields = [
            'agendamento', 'sintomas', 'diagnostico', 'tratamento',
            'observacoes', 'receita', 'valor', 'pago'
        ]
        widgets = {
            'agendamento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'sintomas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Sintomas relatados pelo paciente'
            }),
            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Diagnóstico médico'
            }),
            'tratamento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tratamento prescrito'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observações adicionais'
            }),
            'receita': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Receita médica'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'pago': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_valor(self):
        """Validação do valor"""
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor < 0:
            raise forms.ValidationError("O valor não pode ser negativo")
        return valor

class CustomUserCreationForm(UserCreationForm):
    """Formulário personalizado para criação de usuários"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@exemplo.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user
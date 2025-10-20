from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

class Paciente(models.Model):
    """Modelo para pacientes do consultório"""
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome Completo")
    cpf = models.CharField(
        max_length=14, 
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
            message='CPF deve estar no formato: 000.000.000-00'
        )],
        verbose_name="CPF"
    )
    rg = models.CharField(max_length=20, blank=True, verbose_name="RG")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    endereco = models.TextField(blank=True, verbose_name="Endereço")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    
    # Campos de controle
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def idade(self):
        """Calcula a idade do paciente"""
        hoje = timezone.now().date()
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))

class Profissional(models.Model):
    """Modelo para profissionais do consultório"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, verbose_name="Nome Completo")
    especialidade = models.CharField(max_length=100, verbose_name="Especialidade")
    crm = models.CharField(max_length=20, unique=True, verbose_name="CRM")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail")
    
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
        ordering = ['nome']
    
    def __str__(self):
        return f"Dr(a). {self.nome}"

class Agendamento(models.Model):
    """Modelo para agendamentos de consultas"""
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
        ('faltou', 'Paciente Faltou'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, verbose_name="Profissional")
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado', verbose_name="Status")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['data_hora']
        unique_together = ['profissional', 'data_hora']  # Evita duplo agendamento
    
    def __str__(self):
        return f"{self.paciente.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

class Consulta(models.Model):
    """Modelo para consultas realizadas"""
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, verbose_name="Agendamento")
    sintomas = models.TextField(verbose_name="Sintomas Relatados")
    diagnostico = models.TextField(verbose_name="Diagnóstico")
    tratamento = models.TextField(verbose_name="Tratamento Prescrito")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    receita = models.TextField(blank=True, verbose_name="Receita Médica")
    
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Consulta")
    pago = models.BooleanField(default=False, verbose_name="Pago")
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Consulta: {self.agendamento.paciente.nome} - {self.criado_em.strftime('%d/%m/%Y')}"

class Servico(models.Model):
    """Modelo para serviços oferecidos"""
    nome = models.CharField(max_length=200, verbose_name="Nome do Serviço")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
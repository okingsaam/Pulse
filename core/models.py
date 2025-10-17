"""
MODELS.PY - Modelos do Sistema Pulse
====================================
Este arquivo define a estrutura do banco de dados.
Cada classe = uma tabela no banco.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# ==========================================
# MODELO DE USUÁRIO CUSTOMIZADO
# ==========================================
class User(AbstractUser):
    """
    Usuário customizado que estende o User padrão do Django.
    Adiciona campo 'role' para diferenciar Admin de Paciente.
    """
    # Opções de papéis no sistema
    ROLE_CHOICES = (
        ('admin', 'Administrador'),     # Gerencia tudo
        ('paciente', 'Paciente'),       # Só agenda consultas
    )
    
    # Campos adicionais ao User padrão
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='paciente',
        help_text="Define se é admin ou paciente"
    )
    phone = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Telefone do usuário"
    )

    def __str__(self):
        """Como o usuário aparece quando printado"""
        return f"{self.username} ({self.get_role_display()})"

# ==========================================
# MODELO DE PROFISSIONAL (MÉDICOS)
# ==========================================
class Profissional(models.Model):
    """
    Médicos, dentistas, fisioterapeutas, etc.
    Quem oferece os serviços médicos.
    """
    nome = models.CharField(
        max_length=100,
        help_text="Nome completo do profissional"
    )
    especialidade = models.CharField(
        max_length=100,
        help_text="Ex: Cardiologia, Dermatologia, etc."
    )

    def __str__(self):
        """Como aparece na listagem"""
        return f"{self.nome} - {self.especialidade}"

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"

# ==========================================
# MODELO DE SERVIÇO (CONSULTAS/EXAMES)
# ==========================================
class Servico(models.Model):
    """
    Tipos de consulta ou exame que podem ser agendados.
    Ex: Consulta Cardiológica, Raio-X, etc.
    """
    nome = models.CharField(
        max_length=100,
        help_text="Nome do serviço/consulta"
    )
    descricao = models.TextField(
        blank=True,
        help_text="Detalhes sobre o serviço"
    )
    duracao = models.DurationField(
        help_text="Quanto tempo dura o serviço (ex: 1h)"
    )
    preco = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        help_text="Valor em reais"
    )
    
    # RELACIONAMENTO: Cada serviço pertence a 1 profissional
    profissional = models.ForeignKey(
        Profissional, 
        on_delete=models.CASCADE,
        help_text="Profissional que oferece este serviço"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

# ==========================================
# MODELO DE AGENDAMENTO (CONSULTAS MARCADAS)
# ==========================================
class Agendamento(models.Model):
    """
    Consulta marcada por um paciente.
    Conecta: Paciente + Serviço + Profissional + Data/Hora
    """
    # Status possíveis do agendamento
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),       # Aguardando confirmação
        ('confirmado', 'Confirmado'),   # Consulta confirmada
        ('cancelado', 'Cancelado'),     # Consulta cancelada
    )

    # RELACIONAMENTOS (chaves estrangeiras)
    paciente = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Quem agendou a consulta"
    )
    servico = models.ForeignKey(
        Servico, 
        on_delete=models.CASCADE,
        help_text="Que tipo de consulta"
    )
    profissional = models.ForeignKey(
        Profissional, 
        on_delete=models.CASCADE,
        help_text="Com qual médico"
    )
    
    # DADOS DO AGENDAMENTO
    data_hora = models.DateTimeField(
        help_text="Quando acontecerá a consulta"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pendente',
        help_text="Situação atual do agendamento"
    )
    observacoes = models.TextField(
        blank=True,
        help_text="Informações extras do paciente"
    )

    def __str__(self):
        """Como aparece na listagem"""
        return f"{self.paciente.username} - {self.servico.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['-data_hora']  # Mais recentes primeiro

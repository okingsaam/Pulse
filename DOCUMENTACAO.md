"""
DOCUMENTAÇÃO COMPLETA DO SISTEMA PULSE
======================================

VISÃO GERAL:
-----------
O Pulse é um sistema web para agendamento de consultas médicas.
Permite que pacientes agendem consultas e administradores gerenciem
profissionais, serviços e agendamentos.

TECNOLOGIAS UTILIZADAS:
----------------------
- Django 4.2.25 (Framework web Python)
- Django REST Framework (API)
- Bootstrap 5 (Interface)
- SQLite (Banco de dados)
- HTML/CSS/JavaScript (Frontend)

ESTRUTURA DO PROJETO:
--------------------
pulse_project/           # Pasta principal do projeto Django
├── settings.py         # Configurações gerais
├── urls.py            # URLs principais
├── wsgi.py            # Deploy para produção
└── asgi.py            # Deploy assíncrono

core/                   # Aplicação principal
├── models.py          # Estrutura do banco de dados
├── views.py           # Lógica de negócio
├── urls.py            # Rotas da aplicação
├── forms.py           # Formulários
├── admin.py           # Interface administrativa
├── serializers.py     # API REST
└── templates/         # Templates HTML

templates/              # Templates globais
├── base.html          # Template base
└── registration/      # Templates de login/cadastro

MODELOS (BANCO DE DADOS):
------------------------
1. User (Usuário personalizado)
   - username, email, password (campos padrão)
   - role: 'admin' ou 'paciente'
   - phone: telefone

2. Profissional (Médicos)
   - nome: nome completo
   - especialidade: área médica

3. Servico (Tipos de consulta)
   - nome: nome do serviço
   - descricao: detalhes
   - duracao: tempo necessário
   - preco: valor em reais
   - profissional: quem oferece

4. Agendamento (Consultas marcadas)
   - paciente: quem agendou
   - servico: tipo de consulta
   - profissional: médico escolhido
   - data_hora: quando acontecerá
   - status: pendente/confirmado/cancelado
   - observacoes: informações extras

FLUXO DO SISTEMA:
----------------
1. USUÁRIO VISITA "/" (home)
   → Se não logado: página inicial
   → Se logado: redireciona para dashboard

2. CADASTRO ("/register/")
   → Usuário preenche formulário
   → Sistema cria conta como 'paciente'
   → Faz login automático

3. LOGIN ("/login/")
   → Usuário informa username/senha
   → Sistema valida credenciais
   → Redireciona para dashboard

4. DASHBOARD ("/dashboard/")
   → Paciente: vê seus agendamentos
   → Admin: vê estatísticas gerais

5. AGENDAMENTO ("/agendar/")
   → Usuário escolhe serviço, profissional, data
   → Sistema salva agendamento
   → Status inicial: 'pendente'

TIPOS DE USUÁRIO:
----------------
PACIENTE:
- Pode fazer agendamentos
- Vê apenas seus próprios dados
- Acesso limitado às funcionalidades

ADMIN:
- Vê todos os agendamentos
- Pode cadastrar profissionais/serviços
- Acesso total ao sistema
- Acesso à interface admin (/admin/)

URLS PRINCIPAIS:
---------------
/                    → Página inicial
/register/           → Cadastro
/login/              → Login
/logout/             → Logout
/dashboard/          → Painel principal
/agendar/            → Novo agendamento
/agendamentos/       → Lista agendamentos
/profissionais/      → Lista profissionais (admin)
/servicos/           → Lista serviços (admin)
/admin/              → Interface administrativa
/api/                → API REST

API REST ENDPOINTS:
------------------
GET /api/users/           → Lista usuários
GET /api/profissionais/   → Lista profissionais
GET /api/servicos/        → Lista serviços
GET /api/agendamentos/    → Lista agendamentos

POST /api/agendamentos/   → Criar agendamento
PUT /api/agendamentos/1/  → Atualizar agendamento
DELETE /api/agendamentos/1/ → Deletar agendamento

SEGURANÇA:
----------
- Autenticação obrigatória (exceto home/login/register)
- Controle de acesso por roles
- Pacientes veem apenas seus dados
- Admin tem acesso total
- Senhas criptografadas
- CSRF protection ativado

COMO USAR:
----------
1. Acesse http://127.0.0.1:8000/
2. Cadastre-se como paciente OU
3. Faça login como admin (admin/admin123)
4. Explore as funcionalidades!

DADOS DE EXEMPLO:
----------------
Usuário Admin:
- Username: admin
- Senha: admin123

Profissionais:
- Dr. João Silva (Cardiologia)
- Dra. Maria Santos (Dermatologia)
- Dr. Carlos Lima (Ortopedia)
- Dra. Ana Costa (Ginecologia)

Serviços:
- Consulta Cardiológica (R$ 200,00)
- Consulta Dermatológica (R$ 180,00)
- Consulta Ortopédica (R$ 220,00)
- Consulta Ginecológica (R$ 190,00)

COMANDOS ÚTEIS:
--------------
python manage.py runserver          # Iniciar servidor
python manage.py makemigrations     # Criar migrações
python manage.py migrate            # Aplicar migrações
python manage.py createsuperuser    # Criar admin
python manage.py create_sample_data  # Criar dados exemplo

PRÓXIMOS PASSOS:
---------------
- Adicionar validações de horário
- Sistema de notificações
- Calendário visual
- Relatórios
- Histórico médico
- Integração com pagamentos
"""
# 🏥 Pulse - Sistema de Agendamento Médico

<div align="center">
  <img src="https://img.shields.io/badge/Django-4.2.25-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/API-REST-FF6B6B?style=for-the-badge" alt="REST API">
</div>

<div align="center">
  <h3>🚀 Sistema web completo para agendamento de consultas médicas</h3>
  <p><em>Plataforma moderna, segura e responsiva para gestão de clínicas e consultórios</em></p>
</div>

---

## � Sobre o Projeto

O **Pulse** é uma solução completa para digitalização do processo de agendamento médico, desenvolvida com as melhores práticas de desenvolvimento web. O sistema oferece uma interface intuitiva para pacientes agendarem consultas e ferramentas administrativas robustas para gestão de profissionais, serviços e agendamentos.

### ✨ Principais Funcionalidades

- 🔐 **Sistema de Autenticação Completo** - Login, cadastro e controle de acesso
- 👥 **Gestão de Usuários** - Diferenciação entre administradores e pacientes
- 👨‍⚕️ **Cadastro de Profissionais** - Gestão de médicos e especialidades
- 🩺 **Catálogo de Serviços** - Tipos de consulta, preços e durações
- 📅 **Agendamento Inteligente** - Sistema completo de marcação de consultas
- 📊 **Dashboard Personalizado** - Visão específica por tipo de usuário
- 🌐 **API REST Completa** - Endpoints para integração com outras aplicações
- 📱 **Interface Responsiva** - Design adaptável para todos os dispositivos

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 4.2.25** - Framework web Python
- **Django REST Framework** - API REST robusta
- **SQLite** - Banco de dados relacional
- **Python 3.8+** - Linguagem de programação

### Frontend
- **Bootstrap 5** - Framework CSS responsivo
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript** - Interatividade
- **Django Templates** - Sistema de templates

### Outras Tecnologias
- **Django CORS Headers** - Configuração CORS para APIs
- **Django Crispy Forms** - Formulários elegantes
- **Git** - Controle de versão

---

## � Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Git
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/okingsaam/Pulse.git
   cd Pulse
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**
   ```bash
   python manage.py migrate
   ```

5. **Crie dados de exemplo (opcional)**
   ```bash
   python manage.py create_sample_data
   ```

6. **Execute o servidor**
   ```bash
   python manage.py runserver
   ```

7. **Acesse a aplicação**
   ```
   http://127.0.0.1:8000/
   ```

---

## � Credenciais de Acesso

### Administrador
- **Usuário:** `admin`
- **Senha:** `admin123`
- **Acesso:** Gerenciamento completo do sistema

### Novo Usuário
- Cadastre-se em: `/register/`
- Role automático: **Paciente**
- Acesso: Agendamento de consultas pessoais

---

## 📡 API REST

O sistema oferece uma API REST completa para integração com outras aplicações:

### Endpoints Principais
```
GET    /api/users/           # Lista usuários
GET    /api/profissionais/   # Lista profissionais
GET    /api/servicos/        # Lista serviços
GET    /api/agendamentos/    # Lista agendamentos

POST   /api/agendamentos/    # Criar agendamento
PUT    /api/agendamentos/1/  # Atualizar agendamento
DELETE /api/agendamentos/1/  # Deletar agendamento
```

### Autenticação
- **Tipo:** Session Authentication
- **Requerida:** Sim (todas as rotas protegidas)

---

## 🏗️ Arquitetura do Sistema

### Estrutura de Pastas
```
Pulse/
├── core/                    # Aplicação principal
│   ├── models.py           # Modelos do banco de dados
│   ├── views.py            # Lógica de negócio
│   ├── forms.py            # Formulários
│   ├── serializers.py      # Serializers da API
│   ├── urls.py             # Rotas da aplicação
│   └── templates/          # Templates HTML
├── pulse_project/          # Configurações do projeto
│   ├── settings.py         # Configurações Django
│   └── urls.py             # URLs principais
├── templates/              # Templates globais
├── static/                 # Arquivos estáticos
├── manage.py              # Utilitário Django
└── requirements.txt       # Dependências
```

### Modelos de Dados
- **User** - Usuários do sistema (administradores e pacientes)
- **Profissional** - Médicos e especialistas
- **Servico** - Tipos de consulta disponíveis
- **Agendamento** - Consultas marcadas

---

## 🎯 Demonstração

### Para Pacientes
1. Cadastre-se no sistema
2. Faça login
3. Acesse o dashboard personalizado
4. Agende consultas escolhendo profissional e horário
5. Visualize seus agendamentos

### Para Administradores
1. Faça login com credenciais de admin
2. Acesse dashboard com estatísticas completas
3. Gerencie profissionais e serviços
4. Visualize todos os agendamentos
5. Acesse interface administrativa avançada

---

## 🔒 Segurança

- ✅ Autenticação obrigatória para todas as funcionalidades
- ✅ Controle de acesso baseado em roles
- ✅ Proteção CSRF ativada
- ✅ Validação de formulários
- ✅ Sanitização de dados de entrada

---

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**KingSam**
- GitHub: [@okingsaam](https://github.com/okingsaam)
- Projeto: [Pulse](https://github.com/okingsaam/Pulse)

---

## 📞 Suporte

Encontrou um bug ou tem uma sugestão? 
- Abra uma [issue](https://github.com/okingsaam/Pulse/issues)
- Entre em contato através do GitHub

---

<div align="center">
  <p>⭐ Se este projeto foi útil para você, considere dar uma estrela!</p>
  <p>Desenvolvido com ❤️ usando Django</p>
</div>
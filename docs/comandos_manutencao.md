# Comandos de Manutenção do Sistema Pulse

Este documento descreve todos os comandos de manutenção disponíveis no sistema Pulse.

## 📋 Lista de Comandos

### 1. `system_status` - Monitoramento do Sistema

Exibe informações completas sobre o status atual do sistema.

```bash
# Status básico
python manage.py system_status

# Status detalhado (inclui logs recentes e agendamentos)
python manage.py system_status --detailed
```

**Informações exibidas:**
- Data/hora atual e ambiente (desenvolvimento/produção)
- Status da conexão com banco de dados
- Estatísticas de dados (usuários, profissionais, serviços, agendamentos)
- Verificação de diretórios importantes (logs, static, media)
- Performance do sistema (CPU, memória, disco)
- Agendamentos do dia atual

### 2. `backup_system` - Backup Completo

Cria backup completo do sistema incluindo banco de dados, arquivos e logs.

```bash
# Backup no diretório padrão
python manage.py backup_system

# Backup em diretório específico
python manage.py backup_system --output-dir meus_backups
```

**O que é incluído:**
- Banco de dados (formato JSON)
- Arquivos de mídia (se existirem)
- Arquivos estáticos (se existirem)
- Logs do sistema
- Arquivo de informações do backup

### 3. `restore_backup` - Restauração de Backup

Restaura sistema a partir de backup criado anteriormente.

```bash
# Restauração com confirmação
python manage.py restore_backup backups/pulse_backup_20251019_024102

# Restauração forçada (sem confirmação)
python manage.py restore_backup backups/pulse_backup_20251019_024102 --force
```

**⚠️ ATENÇÃO:** Esta operação substitui todos os dados atuais!

### 4. `cleanup_logs` - Limpeza de Logs

Remove logs antigos para economizar espaço em disco.

```bash
# Limpar logs mais antigos que 30 dias (padrão)
python manage.py cleanup_logs

# Limpar logs mais antigos que 7 dias
python manage.py cleanup_logs --days 7

# Visualizar o que seria removido (sem remover)
python manage.py cleanup_logs --dry-run
```

### 5. `daily_maintenance` - Manutenção Automatizada

Executa rotina completa de manutenção diária.

```bash
# Manutenção básica
python manage.py daily_maintenance

# Manutenção com backup
python manage.py daily_maintenance --backup

# Manutenção mantendo apenas 3 dias de logs
python manage.py daily_maintenance --cleanup-days 3
```

**Operações executadas:**
1. Verificação da saúde do sistema
2. Limpeza de logs antigos
3. Otimização do banco de dados (VACUUM para SQLite)
4. Verificação de integridade dos dados
5. Backup (se solicitado)
6. Relatório detalhado da manutenção

## 🔧 Comandos Existentes (Desenvolvidos Anteriormente)

### `create_sample_data` - Dados de Exemplo
```bash
python manage.py create_sample_data
```

### `send_reminders` - Envio de Lembretes
```bash
python manage.py send_reminders
```

## 📅 Rotina de Manutenção Recomendada

### Diária
```bash
python manage.py daily_maintenance --cleanup-days 7
```

### Semanal
```bash
python manage.py backup_system
python manage.py system_status --detailed
```

### Mensal
```bash
python manage.py cleanup_logs --days 30
python manage.py backup_system --output-dir backups_mensais
```

## 🛠️ Solução de Problemas

### Erro de Conexão com Banco
```bash
python manage.py system_status
python manage.py check
```

### Logs Ocupando Muito Espaço
```bash
python manage.py cleanup_logs --dry-run
python manage.py cleanup_logs --days 7
```

### Sistema Lento
```bash
python manage.py daily_maintenance
python manage.py system_status --detailed
```

### Backup/Restauração
```bash
# Criar backup antes de mudanças importantes
python manage.py backup_system

# Restaurar se algo der errado
python manage.py restore_backup [caminho_do_backup]
```

## 📊 Logs de Manutenção

Todas as operações de manutenção são registradas em:
- `logs/maintenance.log` - Log específico das manutenções
- `logs/django.log` - Log geral do sistema
- `logs/pulse.log` - Log da aplicação

## 🔍 Monitoramento Contínuo

Para monitoramento em tempo real, você pode:

1. **Status rápido:**
   ```bash
   python manage.py system_status
   ```

2. **Verificar performance:**
   ```bash
   python manage.py system_status --detailed
   ```

3. **Verificar logs recentes:**
   ```bash
   type logs\django.log | findstr ERROR
   type logs\pulse.log | findstr WARNING
   ```

## 📋 Checklist de Manutenção

- [ ] Executar `daily_maintenance` diariamente
- [ ] Verificar `system_status` regularmente
- [ ] Fazer backup semanal
- [ ] Limpar logs mensalmente
- [ ] Monitorar performance do sistema
- [ ] Verificar integridade dos dados

---

*Para mais informações sobre qualquer comando, use:*
```bash
python manage.py help [nome_do_comando]
```
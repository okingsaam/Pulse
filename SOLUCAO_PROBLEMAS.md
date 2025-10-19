# 🛠️ Guia de Solução de Problemas - Pulse

## 🚨 Problema: "ERR_CONNECTION_REFUSED"

### 📋 **Causas Comuns:**
1. **Servidor Django parado** - O servidor precisa estar rodando
2. **Porta bloqueada** - Firewall ou antivírus bloqueando
3. **Endereço incorreto** - Verificar URL

### ✅ **Soluções Rápidas:**

#### 1. **Verificar se o servidor está rodando:**
```bash
# No terminal, execute:
python manage.py runserver
```

#### 2. **Usar o script automático:**
```bash
# Execute o script otimizado:
python start_server.py
```

#### 3. **Verificar a porta:**
```bash
# Se porta 8000 estiver ocupada, use outra:
python manage.py runserver 127.0.0.1:8080
```

### 🔧 **Comandos Úteis:**

```bash
# Verificar se a porta está em uso (Windows)
netstat -ano | findstr :8000

# Matar processo na porta (se necessário)
taskkill /PID [PID_NUMBER] /F

# Iniciar servidor em modo debug
python manage.py runserver --debug
```

### 🌐 **URLs do Sistema:**
- **Dashboard Principal:** http://127.0.0.1:8000/consultorio/
- **Pacientes:** http://127.0.0.1:8000/consultorio/pacientes/
- **Agenda:** http://127.0.0.1:8000/consultorio/agenda/
- **Financeiro:** http://127.0.0.1:8000/consultorio/financeiro/
- **Admin Django:** http://127.0.0.1:8000/admin/

### 🛡️ **Prevenção:**

1. **Sempre use o VS Code Task:**
   - `Ctrl+Shift+P` → "Tasks: Run Task" → "Iniciar Servidor Pulse"

2. **Não feche o terminal do servidor**

3. **Use o script start_server.py para maior estabilidade**

### 🔄 **Reinicialização Automática:**

O servidor Django tem auto-reload, mas se parar:
```bash
# Método 1: Script otimizado
python start_server.py

# Método 2: Comando direto
python manage.py runserver 127.0.0.1:8000

# Método 3: Task do VS Code
Ctrl+Shift+P → Tasks: Run Task → Iniciar Servidor Pulse
```

### 📞 **Se o problema persistir:**
1. Reinicie o VS Code
2. Verifique seu firewall/antivírus
3. Execute: `python manage.py check`
4. Execute: `python manage.py migrate`

---
**💜 Sistema Pulse - Interface Médica Moderna**
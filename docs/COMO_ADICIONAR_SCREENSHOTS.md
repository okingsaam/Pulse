# Como Adicionar Screenshots ao README

## 📷 Screenshots Necessárias

Para completar a documentação do projeto, você precisa adicionar as seguintes screenshots na pasta `docs/screenshots/`:

### 1. dashboard.png
- **URL**: http://127.0.0.1:8000/consultorio/
- **Capturar**: Dashboard completo com gráficos e estatísticas
- **Resolução sugerida**: 1920x1080 ou similar

### 2. agenda.png  
- **URL**: http://127.0.0.1:8000/consultorio/agenda/
- **Capturar**: Página da agenda com horários e estatísticas
- **Resolução sugerida**: 1920x1080 ou similar

### 3. pacientes.png
- **URL**: http://127.0.0.1:8000/consultorio/pacientes/
- **Capturar**: Interface de gestão de pacientes
- **Resolução sugerida**: 1920x1080 ou similar

### 4. admin.png
- **URL**: http://127.0.0.1:8000/admin/
- **Capturar**: Painel administrativo do Django
- **Resolução sugerida**: 1920x1080 ou similar

## 🛠️ Como Capturar

1. **Inicie o servidor**:
   ```bash
   python manage.py runserver
   ```

2. **Acesse cada URL** no navegador

3. **Tire screenshots** usando:
   - **Windows**: Win + Shift + S
   - **Mac**: Cmd + Shift + 4
   - **Linux**: Área de captura do sistema

4. **Salve as imagens** na pasta `docs/screenshots/` com os nomes exatos:
   - `dashboard.png`
   - `agenda.png`  
   - `pacientes.png`
   - `admin.png`

## 📐 Dicas para Boas Screenshots

- **Use resolução alta** (mínimo 1920x1080)
- **Capture tela inteira** para mostrar layout completo
- **Verifique se dados aparecem** nos gráficos e tabelas
- **Use modo desktop** (não mobile) para screenshots principais
- **Certifique-se que sidebar está visível**

## ✅ Verificação

Após adicionar as screenshots, o README exibirá automaticamente as imagens nas seções correspondentes.

As imagens serão referenciadas como:
- `docs/screenshots/dashboard.png`
- `docs/screenshots/agenda.png`
- `docs/screenshots/pacientes.png`
- `docs/screenshots/admin.png`
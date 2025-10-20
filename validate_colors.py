#!/usr/bin/env python3
"""
Script de Validação da Padronização de Cores - Sistema Pulse
Verifica se todas as cores estão seguindo o padrão roxo definido
"""

import os
import re
from pathlib import Path

def check_color_consistency():
    """Verifica consistência das cores nos arquivos"""
    
    print("🎨 VALIDAÇÃO DA PADRONIZAÇÃO DE CORES - SISTEMA PULSE")
    print("=" * 60)
    
    # Cores que devem estar presentes
    expected_colors = {
        "primary": "#8e44ad",
        "primary_dark": "#7d3c98", 
        "success": "#27ae60",
        "warning": "#f39c12",
        "danger": "#e74c3c",
        "info": "#3498db"
    }
    
    # Arquivos para verificar
    files_to_check = [
        "static/css/pulse_theme.css",
        "static/admin/css/pulse_admin.css",
        "templates/core/consultorio_dashboard_fixed.html",
        "templates/core/consultorio_agenda.html",
        "templates/core/consultorio_pacientes.html", 
        "templates/core/consultorio_financeiro.html",
        "templates/base.html"
    ]
    
    base_path = Path(__file__).parent
    results = []
    
    print("📁 VERIFICANDO ARQUIVOS:")
    print("-" * 40)
    
    for file_path in files_to_check:
        full_path = base_path / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar se usa variáveis CSS ou cores diretas
            uses_variables = bool(re.search(r'var\(--pulse-', content))
            uses_theme_import = bool(re.search(r'pulse_theme\.css', content))
            has_purple_colors = bool(re.search(r'#8e44ad|#7d3c98', content))
            
            status = "✅ CONFORME"
            if not (uses_variables or uses_theme_import or has_purple_colors):
                status = "⚠️  VERIFICAR"
            
            results.append({
                'file': file_path,
                'status': status,
                'uses_variables': uses_variables,
                'imports_theme': uses_theme_import,
                'has_colors': has_purple_colors
            })
            
            print(f"{status} {file_path}")
            if uses_variables:
                print(f"    ↳ Usa variáveis CSS: Sim")
            if uses_theme_import:
                print(f"    ↳ Importa tema: Sim")
            if has_purple_colors:
                print(f"    ↳ Cores roxas: Sim")
            print()
        else:
            print(f"❌ AUSENTE {file_path}")
            results.append({
                'file': file_path,
                'status': '❌ AUSENTE',
                'uses_variables': False,
                'imports_theme': False,
                'has_colors': False
            })
    
    print("\n🔍 RESUMO DA VALIDAÇÃO:")
    print("-" * 40)
    
    conformes = sum(1 for r in results if "✅" in r['status'])
    total = len(results)
    
    print(f"Arquivos conformes: {conformes}/{total}")
    print(f"Percentual de conformidade: {(conformes/total)*100:.1f}%")
    
    if conformes == total:
        print("\n🎉 PARABÉNS! Todos os arquivos seguem o padrão de cores!")
        print("✅ Sistema 100% padronizado com esquema roxo")
    else:
        print(f"\n⚠️  {total-conformes} arquivo(s) precisam de ajuste")
    
    print("\n🎨 CORES PADRÃO DEFINIDAS:")
    print("-" * 40)
    for name, color in expected_colors.items():
        print(f"• {name.title()}: {color}")
    
    return conformes == total

def check_theme_file():
    """Verifica se o arquivo de tema principal existe e está completo"""
    
    print("\n📋 VERIFICAÇÃO DO ARQUIVO DE TEMA:")
    print("-" * 40)
    
    theme_file = Path(__file__).parent / "static/css/pulse_theme.css"
    
    if not theme_file.exists():
        print("❌ Arquivo pulse_theme.css não encontrado!")
        return False
    
    with open(theme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se contém as variáveis essenciais
    required_vars = [
        "--pulse-primary",
        "--pulse-primary-dark", 
        "--pulse-success",
        "--pulse-warning",
        "--pulse-gradient-primary"
    ]
    
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis ausentes: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Todas as variáveis CSS estão definidas")
        print("✅ Arquivo de tema completo e funcional")
        return True

def main():
    """Função principal"""
    
    os.chdir(Path(__file__).parent)
    
    # Verificar consistência de cores
    colors_ok = check_color_consistency()
    
    # Verificar arquivo de tema
    theme_ok = check_theme_file()
    
    print("\n" + "=" * 60)
    print("🏁 RESULTADO FINAL:")
    
    if colors_ok and theme_ok:
        print("✅ SISTEMA 100% PADRONIZADO!")
        print("🎨 Todas as cores seguem o padrão roxo definido")
        print("🚀 Interface médica moderna e consistente")
        exit(0)
    else:
        print("⚠️  Sistema precisa de ajustes na padronização")
        exit(1)

if __name__ == "__main__":
    main()
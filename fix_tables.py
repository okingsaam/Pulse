#!/usr/bin/env python
"""
Script para corrigir tabelas do banco
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
django.setup()

from django.db import connection

def fix_tables():
    """Corrigir tabelas com colunas faltantes"""
    cursor = connection.cursor()
    
    try:
        # Adicionar colunas faltantes na tabela core_agendamento
        print("🔧 Adicionando colunas faltantes em core_agendamento...")
        
        try:
            cursor.execute('ALTER TABLE core_agendamento ADD COLUMN criado_em datetime DEFAULT CURRENT_TIMESTAMP;')
            print("✅ Coluna criado_em adicionada")
        except Exception as e:
            print(f"ℹ️  criado_em: {e}")
        
        try:
            cursor.execute('ALTER TABLE core_agendamento ADD COLUMN atualizado_em datetime DEFAULT CURRENT_TIMESTAMP;')
            print("✅ Coluna atualizado_em adicionada")
        except Exception as e:
            print(f"ℹ️  atualizado_em: {e}")
        
        # Verificar outras tabelas que podem ter problemas
        tables_to_check = ['core_paciente', 'core_profissional', 'core_servico']
        
        for table in tables_to_check:
            try:
                cursor.execute(f'PRAGMA table_info({table});')
                columns = [col[1] for col in cursor.fetchall()]
                
                if 'criado_em' not in columns:
                    cursor.execute(f'ALTER TABLE {table} ADD COLUMN criado_em datetime DEFAULT CURRENT_TIMESTAMP;')
                    print(f"✅ Coluna criado_em adicionada em {table}")
                
                if 'atualizado_em' not in columns:
                    cursor.execute(f'ALTER TABLE {table} ADD COLUMN atualizado_em datetime DEFAULT CURRENT_TIMESTAMP;')
                    print(f"✅  Coluna atualizado_em adicionada em {table}")
                    
            except Exception as e:
                print(f"ℹ️  Tabela {table}: {e}")
        
        print("\n🎉 Correções concluídas!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    fix_tables()
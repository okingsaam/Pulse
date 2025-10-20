#!/usr/bin/env python
"""
Script para criar tabelas manualmente no banco
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
django.setup()

from django.db import connection

def create_tables():
    """Criar tabelas manualmente"""
    cursor = connection.cursor()
    
    # SQL para criar tabela core_paciente
    create_paciente = """
    CREATE TABLE IF NOT EXISTS "core_paciente" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "nome" varchar(200) NOT NULL,
        "cpf" varchar(14) NOT NULL UNIQUE,
        "rg" varchar(20) NOT NULL,
        "data_nascimento" date NOT NULL,
        "sexo" varchar(1) NOT NULL,
        "telefone" varchar(20) NOT NULL,
        "email" varchar(254) NOT NULL,
        "endereco" text NOT NULL,
        "observacoes" text NOT NULL,
        "ativo" bool NOT NULL,
        "criado_em" datetime NOT NULL,
        "atualizado_em" datetime NOT NULL
    );
    """
    
    # SQL para criar tabela core_consulta
    create_consulta = """
    CREATE TABLE IF NOT EXISTS "core_consulta" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "agendamento_id" bigint NOT NULL UNIQUE,
        "sintomas" text NOT NULL,
        "diagnostico" text NOT NULL,
        "tratamento" text NOT NULL,
        "observacoes" text NOT NULL,
        "receita" text NOT NULL,
        "valor" decimal NOT NULL,
        "pago" bool NOT NULL,
        "criado_em" datetime NOT NULL,
        FOREIGN KEY ("agendamento_id") REFERENCES "core_agendamento" ("id") DEFERRABLE INITIALLY DEFERRED
    );
    """
    
    try:
        # Executar SQLs
        cursor.execute(create_paciente)
        print("✅ Tabela core_paciente criada")
        
        cursor.execute(create_consulta)
        print("✅ Tabela core_consulta criada")
        
        # Verificar tabelas criadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'core_%';")
        tables = cursor.fetchall()
        print(f"\n📋 Tabelas core encontradas: {[t[0] for t in tables]}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    create_tables()
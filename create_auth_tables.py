#!/usr/bin/env python
"""
Script para criar tabelas de auth do Django
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
django.setup()

from django.db import connection

def create_auth_tables():
    """Criar tabelas de autenticação do Django"""
    cursor = connection.cursor()
    
    try:
        # SQL para criar tabela auth_user
        create_auth_user = """
        CREATE TABLE IF NOT EXISTS "auth_user" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "password" varchar(128) NOT NULL,
            "last_login" datetime NULL,
            "is_superuser" bool NOT NULL,
            "username" varchar(150) NOT NULL UNIQUE,
            "first_name" varchar(150) NOT NULL,
            "last_name" varchar(150) NOT NULL,
            "email" varchar(254) NOT NULL,
            "is_staff" bool NOT NULL,
            "is_active" bool NOT NULL,
            "date_joined" datetime NOT NULL
        );
        """
        
        # SQL para criar tabela auth_group
        create_auth_group = """
        CREATE TABLE IF NOT EXISTS "auth_group" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" varchar(150) NOT NULL UNIQUE
        );
        """
        
        # SQL para criar tabela auth_permission
        create_auth_permission = """
        CREATE TABLE IF NOT EXISTS "auth_permission" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" varchar(255) NOT NULL,
            "content_type_id" integer NOT NULL,
            "codename" varchar(100) NOT NULL,
            FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED
        );
        """
        
        # SQL para criar tabela auth_user_groups
        create_auth_user_groups = """
        CREATE TABLE IF NOT EXISTS "auth_user_groups" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" integer NOT NULL,
            "group_id" integer NOT NULL,
            FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
            FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
        );
        """
        
        # SQL para criar tabela auth_user_user_permissions
        create_auth_user_permissions = """
        CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" integer NOT NULL,
            "permission_id" integer NOT NULL,
            FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
            FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
        );
        """
        
        # SQL para criar tabela auth_group_permissions
        create_auth_group_permissions = """
        CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "group_id" integer NOT NULL,
            "permission_id" integer NOT NULL,
            FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
            FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
        );
        """
        
        # Executar SQLs
        print("🔧 Criando tabelas de autenticação...")
        
        cursor.execute(create_auth_user)
        print("✅ Tabela auth_user criada")
        
        cursor.execute(create_auth_group)
        print("✅ Tabela auth_group criada")
        
        cursor.execute(create_auth_permission)
        print("✅ Tabela auth_permission criada")
        
        cursor.execute(create_auth_user_groups)
        print("✅ Tabela auth_user_groups criada")
        
        cursor.execute(create_auth_user_permissions)
        print("✅ Tabela auth_user_user_permissions criada")
        
        cursor.execute(create_auth_group_permissions)
        print("✅ Tabela auth_group_permissions criada")
        
        print("\n🎉 Tabelas de autenticação criadas!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    create_auth_tables()
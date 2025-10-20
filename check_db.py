import sqlite3
import os

# Conectar ao banco
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Listar todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tabelas no banco:")
    for table in tables:
        print(f"- {table[0]}")
    
    # Verificar se tabela core_paciente existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_paciente';")
    core_table = cursor.fetchall()
    
    if core_table:
        print("\nTabela core_paciente EXISTE")
    else:
        print("\nTabela core_paciente NÃO EXISTE")
    
    conn.close()
else:
    print("Arquivo db.sqlite3 não existe")
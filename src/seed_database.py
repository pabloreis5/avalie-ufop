"""
Script para popular o banco de dados com dados iniciais.
Lê os dados de arquivos CSV na pasta data/ e insere no banco.
"""

import sqlite3
import csv
import os
from pathlib import Path

DATABASE = "app.db"
DATA_DIR = Path(__file__).parent / "data"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas do banco de dados"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS curso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplina (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            curso_id INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            curso_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            professor_id INTEGER NOT NULL,
            nota INTEGER NOT NULL CHECK(nota >= 0 AND nota <= 5),
            comentario TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✓ Tabelas criadas com sucesso")


def seed_cursos():
    """Popula a tabela de cursos a partir do arquivo CSV"""
    conn = get_db()
    cursor = conn.cursor()

    csv_path = DATA_DIR / "cursos.csv"
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            cursor.execute(
                "INSERT OR IGNORE INTO curso (nome) VALUES (?)",
                (row['nome'],)
            )
            if cursor.rowcount > 0:
                count += 1

    conn.commit()
    conn.close()
    print(f"✓ {count} cursos inseridos")


def seed_professores():
    """Popula a tabela de professores a partir do arquivo CSV"""
    conn = get_db()
    cursor = conn.cursor()

    csv_path = DATA_DIR / "professores.csv"
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            cursor.execute(
                "INSERT OR IGNORE INTO professor (nome) VALUES (?)",
                (row['nome'],)
            )
            if cursor.rowcount > 0:
                count += 1

    conn.commit()
    conn.close()
    print(f"✓ {count} professores inseridos")


def seed_disciplinas():
    """Popula a tabela de disciplinas a partir dos arquivos CSV"""
    conn = get_db()
    cursor = conn.cursor()

    # Busca todos os arquivos CSV de disciplinas
    disciplinas_files = list(DATA_DIR.glob("disciplinas_*.csv"))
    
    total_count = 0
    for csv_path in disciplinas_files:
        print(f"\nProcessando: {csv_path.name}")
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            
            for row in reader:
                # Busca o ID do curso
                cursor.execute(
                    "SELECT id FROM curso WHERE nome = ?",
                    (row['curso'],)
                )
                result = cursor.fetchone()
                
                if not result:
                    print(f"  ⚠ Curso '{row['curso']}' não encontrado. Pulando disciplina {row['codigo']}")
                    continue
                
                curso_id = result['id']
                nome_completo = f"{row['codigo']} - {row['nome']}"
                
                # Verifica se já existe
                cursor.execute(
                    "SELECT 1 FROM disciplina WHERE nome = ? AND curso_id = ?",
                    (nome_completo, curso_id)
                )
                
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO disciplina (nome, curso_id) VALUES (?, ?)",
                        (nome_completo, curso_id)
                    )
                    count += 1
            
            print(f"  ✓ {count} disciplinas inseridas")
            total_count += count

    conn.commit()
    conn.close()
    print(f"\n✓ Total: {total_count} disciplinas inseridas")


def show_stats():
    """Mostra estatísticas do banco de dados"""
    conn = get_db()
    cursor = conn.cursor()

    print("\n" + "="*50)
    print("ESTATÍSTICAS DO BANCO DE DADOS")
    print("="*50)

    cursor.execute("SELECT COUNT(*) FROM curso")
    print(f"Cursos cadastrados: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM professor")
    print(f"Professores cadastrados: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM disciplina")
    print(f"Disciplinas cadastradas: {cursor.fetchone()[0]}")

    # Disciplinas por curso
    cursor.execute("""
        SELECT c.nome, COUNT(d.id) as total
        FROM curso c
        LEFT JOIN disciplina d ON c.id = d.curso_id
        GROUP BY c.nome
        ORDER BY total DESC
    """)
    
    print("\nDisciplinas por curso:")
    for row in cursor.fetchall():
        print(f"  - {row['nome']}: {row['total']}")

    conn.close()
    print("="*50 + "\n")


def main():
    """Executa o processo completo de seed"""
    print("\n🌱 Iniciando seed do banco de dados...\n")
    
    # Verifica se o diretório de dados existe
    if not DATA_DIR.exists():
        print(f"❌ Erro: Diretório {DATA_DIR} não encontrado")
        return

    # Cria as tabelas
    init_db()
    
    # Popula os dados
    seed_cursos()
    seed_professores()
    seed_disciplinas()
    
    # Mostra estatísticas
    show_stats()
    
    print("✅ Seed concluído com sucesso!\n")


if __name__ == "__main__":
    main()

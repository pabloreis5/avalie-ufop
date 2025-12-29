import sqlite3
from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)
DATABASE = "app.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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
            nota INTEGER NOT NULL,
            comentario TEXT
        )
    """)

    conn.commit()
    conn.close()

def seed_data():
    conn = get_db()
    cursor = conn.cursor()

    cursos = [
        "Engenharia Elétrica",
        "Engenharia de Computação",
        "Engenharia de Produção",
        "Sistemas de Informação"
    ]

    for curso in cursos:
        cursor.execute(
            "INSERT OR IGNORE INTO curso (nome) VALUES (?)",
            (curso,)
        )

    professores = [
        "Professor A",
        "Professor B",
        "Professor C",
        "Professor D"
    ]

    for prof in professores:
        cursor.execute(
            "INSERT OR IGNORE INTO professor (nome) VALUES (?)",
            (prof,)
        )

    disciplinas = [
        ("Cálculo I", 1),
        ("Física I", 1),
        ("Algoritmos", 2),
        ("Estruturas de Dados", 2),
        ("Gestão da Produção", 3),
        ("Pesquisa Operacional", 3),
        ("Banco de Dados", 4),
        ("Engenharia de Software", 4),
    ]

    for nome, curso_id in disciplinas:
        cursor.execute(
            "INSERT OR IGNORE INTO disciplina (nome, curso_id) VALUES (?, ?)",
            (nome, curso_id)
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/avaliar", methods=["GET", "POST"])
def avaliar():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        curso_id = request.form["curso_id"]
        disciplina_id = request.form["disciplina_id"]
        professor_id = request.form["professor_id"]
        nota = request.form["nota"]
        comentario = request.form["comentario"]

        cursor.execute("""
            INSERT INTO avaliacao
            (curso_id, disciplina_id, professor_id, nota, comentario)
            VALUES (?, ?, ?, ?, ?)
        """, (curso_id, disciplina_id, professor_id, nota, comentario))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM curso")
    cursos = cursor.fetchall()

    cursor.execute("SELECT * FROM disciplina")
    disciplinas = cursor.fetchall()

    cursor.execute("SELECT * FROM professor")
    professores = cursor.fetchall()

    conn.close()

    return render_template(
        "avaliar.html",
        cursos=cursos,
        disciplinas=disciplinas,
        professores=professores
    )

@app.route("/avaliacoes")
def avaliacoes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM avaliacao")
    dados = cursor.fetchall()
    conn.close()
    return str([dict(a) for a in dados])

if __name__ == "__main__":
    init_db()
    seed_data()
    app.run(debug=True)

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
DATABASE = "app.db"

DISCIPLINAS_SI = [
    ("CEA059", "Fundamentos de Geometria Analítica e Álgebra Linear"),
    ("CEA060", "Fundamentos de Cálculo"),
    ("CSI101", "Programação de Computadores I"),
    ("CSI601", "Fundamentos de Sistema de Informação"),
    ("CSI901", "Informática e Sociedade"),
    ("CSI902", "Metodologia de Pesquisa"),
    ("CSI011", "Matemática Discreta"),
    ("CSI102", "Programação de Computadores II"),
    ("CSI103", "Algoritmos e Estruturas de Dados I"),
    ("CSI807", "Gestão da Informação"),
    ("ENP144", "Teoria Geral da Administração"),
    ("CEA055", "Estatística e Probabilidade"),
    ("CSI104", "Algoritmos e Estruturas de Dados II"),
    ("CSI115", "Algoritmos e Estruturas de Dados III"),
    ("CSI211", "Fundamentos de Organização e Arquitetura de Computadores"),
    ("ENP473", "Comportamento Organizacional"),
    ("CSI204", "Sistemas Operacionais"),
    ("CSI412", "Engenharia de Software I"),
    ("CSI602", "Banco de Dados I"),
    ("ENP012", "Programação Linear e Inteira"),
    ("ENP150", "Economia"),
    ("CSI106", "Fundamentos Teóricos da Computação"),
    ("CSI301", "Redes de Computadores I"),
    ("CSI410", "Engenharia de Software II"),
    ("CSI522", "Interação Humano-Computador"),
    ("CSI701", "Inteligência Artificial"),
    ("CSI990", "Projeto Integrador I"),
    ("CSI114", "Linguagens de Programação"),
    ("CSI302", "Sistemas Distribuídos"),
    ("CSI405", "Gerência de Projetos de Software"),
    ("CSI606", "Sistemas Web I"),
    ("CSI991", "Projeto Integrador II"),
    ("CSI808", "Gestão da Tecnologia da Informação"),
    ("CSI992", "Trabalho de Conclusão de Curso I"),
    ("ENP026", "Administração de Recursos Humanos"),
    ("ENP493", "Empreendedorismo"),
    ("CSI307", "Segurança e Auditoria de Sistemas"),
    ("CSI605", "Sistemas de Apoio à Decisão"),
    ("CSI997", "Trabalho de Conclusão de Curso II"),
]


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
            nota INTEGER NOT NULL CHECK(nota >= 0 AND nota <= 5),
            comentario TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    # Pega o id do curso "Sistemas de Informação" sem assumir número fixo
    cursor.execute("SELECT id FROM curso WHERE nome = ?", ("Sistemas de Informação",))
    row = cursor.fetchone()
    if not row:
        raise RuntimeError("Curso 'Sistemas de Informação' não encontrado no seed.")
    si_id = row["id"]

    # Insere todas as disciplinas de SI (sem duplicar)
    for codigo, nome in DISCIPLINAS_SI:
        nome_completo = f"{codigo} - {nome}"

        cursor.execute(
            "SELECT 1 FROM disciplina WHERE nome = ? AND curso_id = ?",
            (nome_completo, si_id)
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                "INSERT INTO disciplina (nome, curso_id) VALUES (?, ?)",
                (nome_completo, si_id)
            )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    # Estatísticas
    cursor.execute("SELECT COUNT(*) FROM avaliacao")
    total_avaliacoes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT disciplina_id) FROM avaliacao")
    disciplinas_avaliadas = cursor.fetchone()[0]
    
    cursor.execute("SELECT ROUND(AVG(nota), 2) FROM avaliacao")
    media_geral = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return render_template(
        "index.html",
        total_avaliacoes=total_avaliacoes,
        disciplinas_avaliadas=disciplinas_avaliadas,
        media_geral=media_geral
    )

@app.route("/avaliar", methods=["GET", "POST"])
def avaliar():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        print("DEBUG form:", dict(request.form))

        curso_id = request.form.get("curso_id", "").strip()
        disciplina_id = request.form.get("disciplina_id", "").strip()
        professor_id = request.form.get("professor_id", "").strip()
        nota = request.form.get("nota", "").strip()
        comentario = request.form.get("comentario", "").strip() or None

        # Validação obrigatória (não depende do JS)
        if not (curso_id and disciplina_id and professor_id and nota):
            conn.close()
            flash("Por favor, preencha todos os campos obrigatórios.", "error")
            return redirect(url_for("avaliar"))

        try:
            nota_int = int(nota)
        except ValueError:
            conn.close()
            flash("Nota inválida. Selecione uma nota entre 0 e 5.", "error")
            return redirect(url_for("avaliar"))

        if nota_int < 0 or nota_int > 5:
            conn.close()
            flash("Nota inválida. Selecione uma nota entre 0 e 5.", "error")
            return redirect(url_for("avaliar"))
        
        # Validação de tamanho do comentário
        if comentario and len(comentario) > 500:
            conn.close()
            flash("O comentário deve ter no máximo 500 caracteres.", "error")
            return redirect(url_for("avaliar"))

        cursor.execute("""
            INSERT INTO avaliacao
            (curso_id, disciplina_id, professor_id, nota, comentario)
            VALUES (?, ?, ?, ?, ?)
        """, (curso_id, disciplina_id, professor_id, nota_int, comentario or None))

        conn.commit()
        conn.close()
        
        flash("Avaliação enviada com sucesso! Obrigado pelo seu feedback.", "success")
        return redirect(url_for("index"))


    cursor.execute("SELECT * FROM curso")
    cursos = cursor.fetchall()

    cursor.execute("SELECT id, nome, curso_id FROM disciplina ORDER BY nome")
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

@app.route("/ranking")
def ranking():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            d.nome AS disciplina,
            CASE c.nome
                WHEN 'Sistemas de Informação' THEN 'SI'
                WHEN 'Engenharia Elétrica' THEN 'E.E'
                WHEN 'Engenharia de Computação' THEN 'E.C'
                WHEN 'Engenharia de Produção' THEN 'E.P'
                ELSE c.nome
            END AS curso,
            p.nome AS professor,
            ROUND(AVG(a.nota), 2) AS media,
            COUNT(a.id) AS total_avaliacoes
        FROM avaliacao a
        JOIN disciplina d ON d.id = a.disciplina_id
        JOIN curso c ON c.id = d.curso_id
        JOIN professor p ON p.id = a.professor_id
        GROUP BY d.id, p.id
        ORDER BY media DESC, total_avaliacoes DESC
    """)

    ranking = cursor.fetchall()
    conn.close()

    return render_template("ranking.html", ranking=ranking)


if __name__ == "__main__":
    init_db()

    # Só roda seed se estiver vazio
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM curso")
    empty = (cur.fetchone()[0] == 0)
    conn.close()

    if empty:
        seed_data()

    app.run(debug=True)




import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
import secrets
from datetime import datetime, timedelta
import hashlib


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
DATABASE = "app.db"

# Configurações anti-spam
RATE_LIMIT_MINUTES = 5  # Tempo mínimo entre avaliações
MAX_AVALIACOES_POR_DIA = 10  # Máximo de avaliações por dia


def get_db():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_hash():
    """Gera um hash único baseado no IP e User-Agent do usuário"""
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    unique_string = f"{user_ip}:{user_agent}"
    return hashlib.sha256(unique_string.encode()).hexdigest()


def check_rate_limit():
    """Verifica se o usuário está dentro do limite de avaliações"""
    user_hash = get_user_hash()
    conn = get_db()
    cursor = conn.cursor()
    
    # Buscar último registro do usuário
    cursor.execute("""
        SELECT last_action, action_count 
        FROM rate_limit 
        WHERE user_hash = ?
        ORDER BY last_action DESC 
        LIMIT 1
    """, (user_hash,))
    
    result = cursor.fetchone()
    
    if result:
        last_action = datetime.fromisoformat(result['last_action'])
        action_count = result['action_count']
        now = datetime.now()
        
        # Verificar se passou tempo suficiente desde última ação
        time_diff = (now - last_action).total_seconds() / 60
        
        if time_diff < RATE_LIMIT_MINUTES:
            conn.close()
            return False, f"Aguarde {int(RATE_LIMIT_MINUTES - time_diff)} minuto(s) antes de avaliar novamente."
        
        # Verificar limite diário (últimas 24h)
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM rate_limit
            WHERE user_hash = ?
            AND last_action >= datetime('now', '-1 day')
        """, (user_hash,))
        
        daily_count = cursor.fetchone()['count']
        
        if daily_count >= MAX_AVALIACOES_POR_DIA:
            conn.close()
            return False, f"Limite diário de {MAX_AVALIACOES_POR_DIA} avaliações atingido. Tente novamente amanhã."
    
    conn.close()
    return True, None


def register_rate_limit():
    """Registra uma ação do usuário para controle de rate limit"""
    user_hash = get_user_hash()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO rate_limit (user_hash, last_action, action_count)
        VALUES (?, datetime('now'), 1)
    """, (user_hash,))
    
    conn.commit()
    conn.close()


def init_db():
    """Cria as tabelas do banco de dados se não existirem"""
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_hash TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rate_limit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_hash TEXT NOT NULL,
            last_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            action_count INTEGER DEFAULT 1
        )
    """)

    # Criar índices para melhor performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_rate_limit_hash 
        ON rate_limit(user_hash)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_avaliacao_disciplina 
        ON avaliacao(disciplina_id)
    """)

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
        # Verificar rate limit
        allowed, message = check_rate_limit()
        if not allowed:
            conn.close()
            flash(message, "error")
            return redirect(url_for("avaliar"))

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

        user_hash = get_user_hash()

        cursor.execute("""
            INSERT INTO avaliacao
            (curso_id, disciplina_id, professor_id, nota, comentario, user_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (curso_id, disciplina_id, professor_id, nota_int, comentario or None, user_hash))

        conn.commit()
        conn.close()
        
        # Registrar no rate limit
        register_rate_limit()
        
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

    # Obter parâmetros de filtro e paginação
    curso_filter = request.args.get("curso", "")
    nota_min = request.args.get("nota_min", type=float, default=0)
    aval_min = request.args.get("aval_min", type=int, default=1)
    page = request.args.get("page", type=int, default=1)
    per_page = 20

    # Construir query com filtros
    query = """
        SELECT
            d.id as disciplina_id,
            d.nome AS disciplina,
            c.nome AS curso_completo,
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
        WHERE 1=1
    """
    
    params = []
    
    # Aplicar filtro de curso
    if curso_filter:
        query += " AND c.nome = ?"
        params.append(curso_filter)
    
    query += """
        GROUP BY d.id, p.id
        HAVING AVG(a.nota) >= ? AND COUNT(a.id) >= ?
        ORDER BY media DESC, total_avaliacoes DESC
    """
    
    params.extend([nota_min, aval_min])
    
    # Executar query para contar total
    count_query = f"""
        SELECT COUNT(*) as total FROM (
            {query}
        )
    """
    cursor.execute(count_query, params)
    total_items = cursor.fetchone()['total']
    
    # Calcular paginação
    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page
    
    # Adicionar LIMIT e OFFSET
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    
    cursor.execute(query, params)
    ranking = cursor.fetchall()
    
    # Buscar lista de cursos para o filtro
    cursor.execute("SELECT DISTINCT nome FROM curso ORDER BY nome")
    cursos = [row['nome'] for row in cursor.fetchall()]
    
    conn.close()

    return render_template(
        "ranking.html",
        ranking=ranking,
        cursos=cursos,
        curso_filter=curso_filter,
        nota_min=nota_min,
        aval_min=aval_min,
        page=page,
        total_pages=total_pages,
        total_items=total_items,
        per_page=per_page
    )


@app.route("/api/ranking/suggestions")
def ranking_suggestions():
    """API endpoint que retorna sugestões de busca"""
    query = request.args.get("q", "").strip().lower()
    
    if not query or len(query) < 2:
        return {"suggestions": []}
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Busca disciplinas e professores que correspondem ao termo
    cursor.execute("""
        SELECT DISTINCT d.nome AS text, 'disciplina' AS type
        FROM disciplina d
        WHERE LOWER(d.nome) LIKE ?
        UNION
        SELECT DISTINCT p.nome AS text, 'professor' AS type
        FROM professor p
        WHERE LOWER(p.nome) LIKE ?
        LIMIT 10
    """, (f"%{query}%", f"%{query}%"))
    
    suggestions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"suggestions": suggestions}


if __name__ == "__main__":
    init_db()
    app.run(debug=True)




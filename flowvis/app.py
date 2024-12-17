import calendar
from datetime import datetime
import re
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import hashlib
import mysql.connector

app = Flask(__name__)

app.secret_key = "secret"

def conexao_abrir():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password= "admin",
        database="flowvis"
        )

def verificar_usuario_existente(email, username):
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)
    
    query_email = "SELECT * FROM usuario WHERE usuario_email = %s"
    cursor.execute(query_email, (email,))
    email_existente = cursor.fetchone()

    query_username = "SELECT * FROM usuario WHERE usuario_user = %s"
    cursor.execute(query_username, (username,))
    username_existente = cursor.fetchone()

    cursor.close()
    con.close()

    return email_existente, username_existente

def cadastrar_usuario(u):
    con = conexao_abrir()
    cursor = con.cursor()

    senha_hash = hashlib.sha512(u['password'].encode('utf-8')).hexdigest()

    query = "INSERT INTO usuario (usuario_nome, usuario_user, usuario_email, usuario_senha) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (u['usuario_nome'], u['usuario_user'], u['usuario_email'], senha_hash))

    con.commit()
    cursor.close()
    con.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if validar_usuario(email, password):
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        nome = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        email_existente, username_existente = verificar_usuario_existente(email, username)

        if email_existente:
            return render_template("signin.html", error="O e-mail já está cadastrado.")
        
        if username_existente:
            return render_template("signin.html", error="O nome de usuário já está em uso.")

        password_validation = password_check(password)
        if not password_validation['password_ok']:
            error_messages = []
            if password_validation['length_error']:
                error_messages.append("A senha deve ter pelo menos 8 caracteres.")
            if password_validation['digit_error']:
                error_messages.append("A senha deve conter pelo menos um dígito.")
            if password_validation['uppercase_error']:
                error_messages.append("A senha deve conter pelo menos uma letra maiúscula.")
            if password_validation['lowercase_error']:
                error_messages.append("A senha deve conter pelo menos uma letra minúscula.")
            if password_validation['symbol_error']:
                error_messages.append("A senha deve conter pelo menos um símbolo.")

            return render_template("signin.html", error="<br>".join(error_messages))

        cadastrar_usuario({
            "usuario_nome": nome,
            "usuario_user": username,
            "usuario_email": email,
            "password": password
        })

        return redirect(url_for("login"))
    return render_template("signin.html")

@app.route("/home")
def home():
    if 'user' not in session:
        return redirect(url_for("login"))
    
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)
    
    query = """
    SELECT p.post_id AS id, p.content, p.created_at, 
       p.curtidas_count, u.usuario_nome, u.usuario_user
    FROM post p
    JOIN usuario u ON p.user_id = u.usuario_id
    ORDER BY p.created_at DESC
    """
    cursor.execute(query)
    posts = cursor.fetchall()
    
    cursor.close()
    con.close()

    return render_template("home.html", posts=posts, user=session['user'])

def validar_usuario(email, password):
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query = "SELECT * FROM usuario WHERE usuario_email = %s"
    cursor.execute(query, (email,))
    usuario = cursor.fetchone()

    cursor.close()
    con.close()

    if usuario and usuario['usuario_senha'] == hashlib.sha512(password.encode('utf-8')).hexdigest():
        session['user'] = usuario['usuario_nome']
        session['user_id'] = usuario['usuario_id']

        return True
    return False

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/post", methods=["POST"])
def criar_post():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    conteudo = request.form.get("content")
    if not conteudo.strip():
        return redirect(url_for("home", error="Post não pode estar vazio!"))

    con = conexao_abrir()
    cursor = con.cursor()
    query = "INSERT INTO post (user_id, content) VALUES (%s, %s)"
    cursor.execute(query, (session['user_id'], conteudo))
    con.commit()

    cursor.close()
    con.close()
    return redirect(url_for("home"))


@app.route("/posts", methods=["GET"])
def listar_posts():
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query = """
    SELECT p.post_id AS id, p.content, p.created_at, 
           u.usuario_nome, u.usuario_user,
           (SELECT COUNT(*) FROM curtidas WHERE post_id = p.post_id) AS curtidas_count,
           (SELECT COUNT(*) FROM curtidas WHERE user_id = %s AND post_id = p.post_id) AS user_curtida
    FROM post p
    JOIN usuario u ON p.user_id = u.usuario_id
    ORDER BY p.created_at DESC
    """
    cursor.execute(query, (session['user_id'],))
    posts = cursor.fetchall()

    cursor.close()
    con.close()
    return render_template("home.html", posts=posts)


@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Usuário não autenticado"}), 401

    user_id = session['user_id']
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query_check_like = "SELECT * FROM curtidas WHERE user_id = %s AND post_id = %s"
    cursor.execute(query_check_like, (user_id, post_id))
    curtida = cursor.fetchone()

    if curtida:
        query_remove_like = "DELETE FROM curtidas WHERE user_id = %s AND post_id = %s"
        cursor.execute(query_remove_like, (user_id, post_id))
        action = "removed"
    else:
        query_add_like = "INSERT INTO curtidas (user_id, post_id) VALUES (%s, %s)"
        cursor.execute(query_add_like, (user_id, post_id))
        action = "added"

    query_count_likes = "SELECT COUNT(*) AS curtidas_count FROM curtidas WHERE post_id = %s"
    cursor.execute(query_count_likes, (post_id,))
    curtidas_count = cursor.fetchone()["curtidas_count"]

    query_update_post_likes = "UPDATE post SET curtidas_count = %s WHERE post_id = %s"
    cursor.execute(query_update_post_likes, (curtidas_count, post_id))

    con.commit()
    cursor.close()
    con.close()

    return jsonify({"success": True, "action": action, "curtidas_count": curtidas_count})

@app.route("/grupo/<int:grupo_id>/like/<int:post_id>", methods=["POST"])
def like_post_grupo(grupo_id, post_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Usuário não autenticado"}), 401

    user_id = session['user_id']
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query_check_like = "SELECT * FROM curtidas WHERE user_id = %s AND post_id = %s"
    cursor.execute(query_check_like, (user_id, post_id))
    curtida = cursor.fetchone()

    if curtida:
        query_remove_like = "DELETE FROM curtidas WHERE user_id = %s AND post_id = %s"
        cursor.execute(query_remove_like, (user_id, post_id))
        action = "removed"
    else:
        query_add_like = "INSERT INTO curtidas (user_id, post_id) VALUES (%s, %s)"
        cursor.execute(query_add_like, (user_id, post_id))
        action = "added"

    query_count_likes = "SELECT COUNT(*) AS curtidas_count FROM curtidas WHERE post_id = %s"
    cursor.execute(query_count_likes, (post_id,))
    curtidas_count = cursor.fetchone()["curtidas_count"]

    query_update_post_likes = "UPDATE post_grupo SET curtidas_count = %s WHERE post_id = %s"
    cursor.execute(query_update_post_likes, (curtidas_count, post_id))

    con.commit()
    cursor.close()
    con.close()

    return jsonify({"success": True, "action": action, "curtidas_count": curtidas_count})



def criar_grupo_bd(nome, imagem, criador_id):
    con = conexao_abrir()
    cursor = con.cursor()

    query = "INSERT INTO grupos (nome, imagem, criador_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (nome, imagem, criador_id))
    con.commit()

    grupo_id = cursor.lastrowid

    query_participante = "INSERT INTO grupo_usuarios (grupo_id, usuario_id) VALUES (%s, %s)"
    cursor.execute(query_participante, (grupo_id, criador_id))
    con.commit()

    cursor.close()
    con.close()


def listar_grupos_bd(usuario_id):
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query = """
    SELECT g.id, g.nome, g.imagem, 
           (SELECT COUNT(*) FROM grupo_usuarios WHERE grupo_id = g.id) AS participantes
    FROM grupos g
    WHERE g.id NOT IN (
        SELECT grupo_id FROM grupo_usuarios WHERE usuario_id = %s
    )
    """
    cursor.execute(query, (usuario_id,))
    grupos = cursor.fetchall()

    cursor.close()
    con.close()
    return grupos

@app.route("/criar-grupo", methods=["POST"])
def criar_grupo():
    if request.method == "POST":
        nome = request.form.get("nome")
        imagem = request.form.get("imagem")

        if not nome or not imagem:
            return render_template("criar_grupo.html", error="Todos os campos são obrigatórios.")

        criador_id = session.get("user_id")
        if not criador_id:
            return redirect(url_for("login"))

        criar_grupo_bd(nome, imagem, criador_id)
        return redirect(url_for("grupos"))

    return render_template("criar_grupo.html")

@app.route("/descubra")
def descubra():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    usuario_id = session['user_id']
    grupos = listar_grupos_bd(usuario_id)
    return render_template("descubra.html", grupos=grupos, user=session.get('user'))

def participar_grupo_bd(grupo_id, usuario_id):
    con = conexao_abrir()
    cursor = con.cursor()

    query = """INSERT IGNORE INTO grupo_usuarios (grupo_id, usuario_id)
               VALUES (%s, %s)"""
    cursor.execute(query, (grupo_id, usuario_id))
    con.commit()

    cursor.close()
    con.close()

def listar_grupos_usuario(usuario_id):
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query = """
    SELECT g.id, g.nome, g.imagem, 
           (SELECT COUNT(*) FROM grupo_usuarios WHERE grupo_id = g.id) AS participantes
    FROM grupo_usuarios gu
    JOIN grupos g ON gu.grupo_id = g.id
    WHERE gu.usuario_id = %s
    """
    cursor.execute(query, (usuario_id,))
    grupos = cursor.fetchall()

    cursor.close()
    con.close()
    return grupos

@app.route("/participar/<int:grupo_id>", methods=["POST"])
def participar_grupo(grupo_id):
    if 'user_id' not in session:
        return redirect(url_for("login"))

    usuario_id = session['user_id']
    participar_grupo_bd(grupo_id, usuario_id)

    return redirect(url_for("grupos"))


@app.route("/grupos")
def grupos():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    usuario_id = session['user_id']
    meus_grupos = listar_grupos_usuario(usuario_id)
    novos_grupos = listar_grupos_bd(usuario_id)

    return render_template("grupos.html", meus_grupos=meus_grupos, novos_grupos=novos_grupos, user=session['user'])

def obter_detalhes_grupo(grupo_id):
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query_grupo = "SELECT id, nome, imagem, criador_id FROM grupos WHERE id = %s"
    cursor.execute(query_grupo, (grupo_id,))
    grupo = cursor.fetchone()

    query_participantes = """
    SELECT u.usuario_nome, u.usuario_user,
           CASE WHEN gu.usuario_id = g.criador_id THEN 1 ELSE 0 END AS is_criador
    FROM grupo_usuarios gu
    JOIN usuario u ON gu.usuario_id = u.usuario_id
    JOIN grupos g ON gu.grupo_id = g.id
    WHERE gu.grupo_id = %s
    """
    cursor.execute(query_participantes, (grupo_id,))
    participantes = cursor.fetchall()

    cursor.close()
    con.close()

    return grupo, participantes


def listar_posts_grupo(grupo_id):
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query = """
    SELECT p.post_id AS id, p.content, p.created_at, 
        (SELECT COUNT(*) FROM curtidas WHERE post_id = p.post_id) AS curtidas_count,
        u.usuario_nome, u.usuario_user
    FROM post_grupo p
    JOIN usuario u ON p.user_id = u.usuario_id
    WHERE p.grupo_id = %s
    ORDER BY p.created_at DESC
    """

    cursor.execute(query, (grupo_id,))
    posts = cursor.fetchall()

    cursor.close()
    con.close()
    return posts

@app.route("/grupo/<int:grupo_id>")
def pagina_grupo(grupo_id):
    if 'user_id' not in session:
        return redirect(url_for("login"))

    grupo, participantes = obter_detalhes_grupo(grupo_id)
    posts = listar_posts_grupo(grupo_id)
    eventos = listar_eventos_grupo(grupo_id)
    return render_template("grupo.html", grupo=grupo, participantes=participantes, posts=posts, eventos=eventos, user=session['user'])


@app.route("/grupo/<int:grupo_id>/postar", methods=["POST"])
def criar_post_grupo(grupo_id):
    if 'user_id' not in session:
        return redirect(url_for("login"))

    conteudo = request.form.get("content")
    if not conteudo.strip():
        return redirect(url_for("pagina_grupo", grupo_id=grupo_id, error="Post não pode estar vazio!"))

    con = conexao_abrir()
    cursor = con.cursor()

    query = "INSERT INTO post_grupo (grupo_id, user_id, content) VALUES (%s, %s, %s)"
    cursor.execute(query, (grupo_id, session['user_id'], conteudo))
    con.commit()

    cursor.close()
    con.close()
    return redirect(url_for("pagina_grupo", grupo_id=grupo_id))

@app.route("/grupo/<int:grupo_id>/criar-evento", methods=["POST"])
def criar_evento(grupo_id):
    if 'user_id' not in session:
        return redirect(url_for("login"))

    usuario_id = session['user_id']
    titulo = request.form.get("titulo")
    data = request.form.get("data")
    local = request.form.get("local")
    descricao = request.form.get("descricao")

    con = conexao_abrir()
    cursor = con.cursor()

    query = """
    INSERT INTO eventos (grupo_id, titulo, data, local, descricao, criador_id) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (grupo_id, titulo, data, local, descricao, usuario_id))
    con.commit()

    cursor.close()
    con.close()

    return redirect(url_for("pagina_grupo", grupo_id=grupo_id))

def listar_eventos_grupo(grupo_id):
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query = """
    SELECT titulo, data, local, descricao
    FROM eventos
    WHERE grupo_id = %s
    ORDER BY data ASC
    """
    cursor.execute(query, (grupo_id,))
    eventos = cursor.fetchall()

    cursor.close()
    con.close()
    return eventos

def listar_eventos_usuario(usuario_id):
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)

    query = """
    SELECT e.titulo AS nome_evento, e.data, e.local, g.nome AS grupo_nome, g.id AS grupo_id
    FROM eventos e
    JOIN grupo_usuarios gu ON e.grupo_id = gu.grupo_id
    JOIN grupos g ON e.grupo_id = g.id
    WHERE gu.usuario_id = %s
    ORDER BY e.data ASC
    """
    cursor.execute(query, (usuario_id,))
    eventos = cursor.fetchall()

    cursor.close()
    con.close()
    return eventos

@app.before_request
def carregar_eventos():
    if 'user_id' in session:
        usuario_id = session['user_id']
        eventos = listar_eventos_usuario(usuario_id)
        session['eventos'] = eventos

@app.route("/meus-eventos")
def meus_eventos():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    usuario_id = session['user_id']

    ano_atual = datetime.now().year
    mes_atual = datetime.now().month

    cal = calendar.monthcalendar(ano_atual, mes_atual)

    eventos = listar_eventos_usuario(usuario_id)

    eventos_por_dia = {}
    for evento in eventos:
        dia_evento = evento['data'].day
        if dia_evento not in eventos_por_dia:
            eventos_por_dia[dia_evento] = []
        eventos_por_dia[dia_evento].append(evento)

    return render_template("meus_eventos.html", 
                           cal=cal, 
                           eventos_por_dia=eventos_por_dia, 
                           mes_atual=mes_atual, 
                           ano_atual=ano_atual, 
                           user=session['user'])

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    """

    length_error = len(password) < 8

    digit_error = re.search(r"\d", password) is None

    uppercase_error = re.search(r"[A-Z]", password) is None

    lowercase_error = re.search(r"[a-z]", password) is None

    symbol_error = re.search(r"[ @!#$%&'()*+,-./[\\\]^_{|}~"+r'"]', password) is None

    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }

app.run(port=5001)
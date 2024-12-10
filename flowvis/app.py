import re
from flask import Flask, redirect, render_template, request, session, url_for
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
    con = conexao_abrir()
    cursor = con.cursor(dictionary=True)
    
    query = """
    SELECT p.content, p.created_at, u.usuario_nome, u.usuario_user
    FROM post p
    JOIN usuario u ON p.user_id = u.usuario_id
    ORDER BY p.created_at DESC
    """
    cursor.execute(query)
    posts = cursor.fetchall()
    
    cursor.close()
    con.close()

    return render_template("home.html", posts=posts)


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
    SELECT p.content, p.created_at, u.usuario_nome, u.usuario_user
    FROM post p
    JOIN usuario u ON p.user_id = u.usuario_id
    ORDER BY p.created_at DESC
    """
    cursor.execute(query)
    posts = cursor.fetchall()

    cursor.close()
    con.close()
    return render_template("home.html", posts=posts)

####################
def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    """

    length_error = len(password) < 8

    digit_error = re.search(r"\d", password) is None

    uppercase_error = re.search(r"[A-Z]", password) is None

    lowercase_error = re.search(r"[a-z]", password) is None

    symbol_error = re.search(r"[ @!#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

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
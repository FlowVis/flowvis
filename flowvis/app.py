from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("inicio.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("inicio.html")

# acho que tem que arrumar aqui:
# @app.route("/")
# def recover_password_page():
#     return render_template("recover_password.html")

# @app.route("/recover_password", methods=["POST"])
# def recover_password():
#     email = request.form.get("email")
#     # Aqui você pode adicionar lógica para envio de e-mail com token de recuperação
#     print(f"Instruções enviadas para: {email}")
#     return redirect(url_for("update_password_page"))

# @app.route("/update_password", methods=["GET", "POST"])
# def update_password_page():
#     if request.method == "POST":
#         new_password = request.form.get("new_password")
#         confirm_password = request.form.get("confirm_password")
#         if new_password == confirm_password:
#             print(f"Senha alterada com sucesso: {new_password}")
#             return "Senha alterada com sucesso!"
#         else:
#             return "As senhas não coincidem, tente novamente."
#   return render_template("recover_password_step2.html")
#

# @app.route("/")
# def profile():
#     # Informações dinâmicas podem ser passadas para o template aqui
#     user_data = {
#         "name": "Alice Maria",
#         "username": "@licemaria",
#         "following": 28,
#         "followers": 168,
#         "suggestions": [
#             {"name": "Alina Boz", "location": "Santa Monica, CA", "username": "@BozAlina", "image": "user1.jpg"},
#             {"name": "Elijah Mikaelson", "location": "Sófia, BG", "username": "@elijahmikael", "image": "user2.jpg"}
#         ],
#         "events": [
#             {"title": "AUTÓDROMO DE INTERLAGOS", "date": "NOVEMBRO 14", "description": "Evento: I-N-C-R-Í-V-E-L", "tags": "#race #formula1", "image": "race.jpg"}
#         ]
#     }
#     return render_template("profile.html", user=user_data)

app.run(port=5001)
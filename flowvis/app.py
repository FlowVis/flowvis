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

app.run(port=5001)
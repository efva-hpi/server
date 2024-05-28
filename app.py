from crypt import methods
from flask import Flask, render_template, request
from markupsafe import escape
from spiellogik import *

app = Flask(__name__)

gs: GameState = GameState()

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/lobby/<id>", methods=["GET", "POST"])
def lobby(id):
    if (request.method == "POST"):
        form = request.form
        code = form.get("lobbyCode")
        n_questions = form.get("numberOfQuestions")
        category = form.get("categorySelect")
        difficulty = form.get("difficultySelect")
        gamemode = form.get("gamemodeSelect")
    return f"<p>Lobby {code}</p><p>Fragen: {n_questions}</p><p>Kategorie: {category}</p><p>Schwierigkeit: {difficulty}</p><p>Spielmodus: {gamemode}</p>"
from crypt import methods
from flask import Flask, render_template, request, redirect
from markupsafe import escape
from spiellogik import *

app = Flask(__name__)

gs: GameState = GameState()
validLobbyKey: bool = True

@app.route("/")
def main_page():
    return render_template("index.html", validLobbyKey=validLobbyKey)

@app.route("/lobby/<code>", methods=["GET", "POST"])
def lobby(code):
    if (request.method == "POST"):
        form = request.form
        if (form.get("lobbyFormType") == "create"):
            game_settings = GameSettings(form.get("numberOfQuestions"), form.get("category"), form.get("difficulty"), form.get("gamemode"))
            gs.create_lobby(code, game_settings)
            return redirect(f"/lobby/{code}")
        elif (form.get("lobbyFormType") == "join"):
            #return render_template("lobby.html", lobbyInfo = form)
            currentLobby = gs.get_lobby_by_code(code)
            if(currentLobby is None):
                redirect("/")
            return redirect(f"/lobby/{code}")
    elif (request.method == "GET"):
        currentLobby = gs.get_lobby_by_code(code)
        return render_template("lobby.html", lobbyInfo = currentLobby.game_settings, lobbyCode = currentLobby.code)
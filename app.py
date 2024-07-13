from crypt import methods
from flask import Flask, render_template, request, redirect, flash, session
from markupsafe import escape
from spiellogik import *
from login import login as a_login, register as a_register, psycopg2Error


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

gs: GameState = GameState()
# validLobbyKey: bool = True

@app.route("/")
def main_page():
    print(session.get('_flashes', None))
    return render_template("index.html")

@app.route("/lobby/<code>", methods=["GET", "POST"])
def lobby(code):
    session.pop('_flashes', None)
    global validLobbyKey
    if request.method == "POST":
        # print("lobby post")
        form = request.form
        if (form.get("lobbyFormType") == "create"):
            # print("creating lobby")
            game_settings = GameSettings(form.get("numberOfQuestions"), form.get("category"), form.get("difficulty"), form.get("gamemode"))
            gs.create_lobby(code, game_settings)
            return redirect(f"/lobby/{code}")
        elif (form.get("lobbyFormType") == "join"):
            # print("joining lobby")
            currentLobby = gs.get_lobby_by_code(code)
            if(currentLobby is None):
                return no_valid_lobby()
            print("lobby found")
            return redirect(f"/lobby/{code}")
    elif (request.method == "GET"):
        # print("lobby get")
        currentLobby = gs.get_lobby_by_code(code)
        if(currentLobby is None):
            return no_valid_lobby()
        print("rendering lobby get")
        return render_template("lobby.html", lobbyInfo = currentLobby.game_settings, lobbyCode = currentLobby.code)

@app.route("/lobby/<code>/leave", methods=["GET", "POST"])
def leave_lobby(code):
    print("leaving lobby")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    try:
        form = request.form
        a_login(form.get("loginUsernameInp"), form.get("loginPasswordInp"))
        return redirect("/")
    except psycopg2Error as e:
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            form = request.form
            a_register(form.get("registerUsernameInp"), form.get("registerPasswordInp"), form.get("registerEmailInp"))
            return redirect("/")
        except psycopg2Error as e:
            flash('Dieser Nutzer hat bereits ein Konto', 'error')
            return redirect("/")

# Hilfsfunktionen
def no_valid_lobby():
    # print("no valid lobby")
    flash('Bitte einen gültigen Lobby code eingeben', 'error')
    return redirect("/")
from crypt import methods
from flask import Flask, render_template, request, redirect, flash, session
from markupsafe import escape
from spiellogik import *
from login import login as a_login, register as a_register, psycopg2Error
import jwt
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

gs: GameState = GameState()
# validLobbyKey: bool = True

@app.route("/")
def main_page():
    auth_token = session.get('auth_token', None)
    if auth_token:
        session.pop('auth_token')
    return render_template("index.html", auth_token=auth_token)

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
            return redirect(f"/lobby/{code}")
    elif (request.method == "GET"):
        # print("lobby get")
        currentLobby = gs.get_lobby_by_code(code)
        if(currentLobby is None):
            return no_valid_lobby()
        return render_template("lobby.html", lobbyInfo = currentLobby.game_settings, lobbyCode = currentLobby.code)

@app.route("/lobby/<code>/leave", methods=["GET", "POST"])
def leave_lobby(code):
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    try:
        form = request.form
        username = form.get("loginUsernameInp")
        password = form.get("loginPasswordInp")
        if not a_login(username, password):
            flash('username oder Passwort ist falsch', error)
            return redirect("/")
        token = generateToken(username)
        session['auth_token'] = token
        return redirect("/")
    except psycopg2Error as e:
        flash('Kein Nutzer unter diesen Daten gefunden', 'error')
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            form = request.form
            username = form.get("registerUsernameInp")
            a_register(username, form.get("registerPasswordInp"), form.get("registerEmailInp"))
            token = generateToken(username)
            session['auth_token'] = token
            return redirect("/")
        except psycopg2Error as e:
            flash('Dieser Nutzer hat bereits ein Konto', 'error')
            return redirect("/")

# Hilfsfunktionen
def no_valid_lobby():
    # print("no valid lobby")
    flash('Bitte einen gültigen Lobby code eingeben', 'error')
    return redirect("/")

def generateToken(username: str):
    return jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3)
        }, app.secret_key, algorithm='HS256')
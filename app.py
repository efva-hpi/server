from crypt import methods
from flask import Flask, render_template, request, redirect, flash, session, Response, make_response
from markupsafe import escape
from spiellogik import *
from login import login as a_login, register as a_register, psycopg2Error
import jwt
import datetime
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)

gs: GameState = GameState()

@app.route("/")
def main_page():
    auth_token = session.get('auth_token', None)
    if auth_token:
        session.pop('auth_token')
    return render_template("index.html", auth_token=auth_token)




@app.route("/lobby/<code>", methods=["GET", "POST"])
def lobby(code):
    session.pop('_flashes', None)
    auth_cookie: str = request.cookies.get('auth_token', None)
    if request.method == "POST":
        form = request.form
        if form.get("lobbyFormType") == "create": # Create a lobby
            if not auth_cookie: # Checks if is logged in
                flash('Please log in or register to create a lobby!', 'error')
                return redirect("/")
            game_settings = GameSettings(
                int(form.get("numberOfQuestions")),
                int(form.get("category")),
                form.get("difficulty"),
                form.get("gamemode")
            )
            gs.create_lobby(code, game_settings)

        elif form.get("lobbyFormType") == "guest": # Guest joining lobby
            current_lobby: Optional[Lobby] = gs.get_lobby_by_code(code)
            if current_lobby is None:
                return no_valid_lobby()
            username: str = form.get("guestUsernameInp")
            players: list[str] = current_lobby.get_player_list()
            if username in players:
                flash('Username existiert bereits', 'message')
                return render_template('lobby.html', lobbyInfo=None, lobbyCode=None, players=None)

            token = generate_token(username, datetime.timedelta(hours=3))
            session['auth_token'] = token

        else: # Joining a lobby
            currentLobby: Optional[Lobby] = gs.get_lobby_by_code(code)
            if currentLobby is None:
                return no_valid_lobby()
        return redirect(f"/lobby/{code}")
    elif request.method == "GET":
        # print("lobby get")
        auth_token = session.get('auth_token', None)
        if auth_token:
            session.pop('auth_token')
            auth_cookie = auth_token
        elif not auth_cookie:
            flash('Please enter a username', 'message')
            return render_template('lobby.html', lobbyInfo=None, lobbyCode=None, players=None)
        decoded_auth_token = decode_token(auth_cookie)
        username = decoded_auth_token['username']
        current_lobby = gs.get_lobby_by_code(code)
        if current_lobby is None:
            return no_valid_lobby()
        joining_player: Player = Player(username)
        current_lobby.add_player(joining_player)
        players: list[str] = current_lobby.get_player_list()
        return render_template("lobby.html", lobbyInfo=current_lobby.game_settings, lobbyCode=current_lobby.code, players=players)


@app.route("/lobby/<code>/leave", methods=["GET", "POST"])
def leave_lobby(code):
    auth_token = request.cookies.get('auth_token', None)
    if not auth_token:
        redirect("/")
    leaving_player_username = decode_token(auth_token)['username']
    current_lobby: Optional[Lobby] = gs.get_lobby_by_code(code)
    if (current_lobby == None): return no_valid_lobby();
    players: list[Player] = current_lobby.get_players()
    leaving_player: Player = next((player for player in players if player.username == leaving_player_username), None)
    current_lobby.remove_player(leaving_player)
    return redirect("/")


@app.route("/lobby/<code>/start", methods=["GET"])
def start_game(code):
    auth_token = request.cookies.get('auth_token', None)
    if not auth_token:
        flash("You must be logged in", "error")
        return redirect("/")
    
    if (gs.get_game_by_id(code) != None): return redirect(f"/game/{code}") # Redirect to game page if already started

    lobby: Optional[Lobby] = gs.get_lobby_by_code(code)
    if lobby == None: 
        flash("Lobby nicht gefunden", "error")
        return redirect("/") # Check if lobby exists
    #if (len(lobby.get_players()) < 2): 
    #    return redirect(f"/lobby/{code}") # Not enough players
    gs.start_game(gs.get_id(code))
    print("Started Game")
    return redirect(f"/game/{code}")


@socketio.on('message')
def on_message(message):
    send(message=message)

@app.route("/game/<code>", methods=["GET"])
def game_page(code):
    auth_token = request.cookies.get('auth_token', None)
    if not auth_token:
        flash("Du bist noch eingeloggt", "error")
        return redirect("/")
    player: Optional[Player] = gs.get_player_by_username(decode_token(auth_token)['username'])
    game: Optional[Game] = gs.get_game_by_id(gs.get_id(code))
    if (game == None): 
        flash(f"Spiel {code} nicht gefunden", "error")
        return redirect("/") # Check if game exists
    
    q: Question = game.get_current_question()
    
    return render_template("game.html", lobbyCode=code, question=q.question, answers=q.answers)


@app.route("/login", methods=["POST"])
def login():
    try:
        form = request.form
        username = form.get("loginUsernameInp")
        password = form.get("loginPasswordInp")
        if not a_login(username, password):
            flash('username oder Passwort ist falsch', 'error')
            return redirect("/")
        token = generate_token(username)
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
            token = generate_token(username)
            session['auth_token'] = token
            return redirect("/")
        except psycopg2Error as e:
            flash('Dieser Nutzer hat bereits ein Konto', 'error')
            return redirect("/")
        

# Hilfsfunktionen
def no_valid_lobby():
    # print("no valid lobby")
    flash('Diese Lobby existiert nicht', 'error')
    return redirect("/")


def generate_token(username: str, lifetime: datetime.timedelta = datetime.timedelta(days=3)):
    return jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + lifetime
    }, app.secret_key, algorithm='HS256')

def decode_token(token: str):
    return jwt.decode(token.encode('UTF-8'), app.secret_key, algorithms=['HS256'])

"""
Player List:    {"id" : 0, "players" : ["Tobi", "Udolf", "Rudolf"], "lobby_code":"JGL486"}
Start game:     {"id" : 1, "lobby_code": "ABF683"}
New question:   {"id" : 2, "question_index" : 0, "question" : "Was los?", "answers" : ["Hö", "Hä", "Hey", "Ha"], "lobby_code" : "HGJ754"}
Submit answers: {"id" : 3, "auth_token" : "...", "question_index" : 0, "answer" : 4, "lobby_code" : "ABC143"}
Get Question:   {"id" : 4, "auth_token" : "...", "lobby_code" : "HFG749"}
End Game:       {"id" : 5, "lobby_code" : "ABC123"}
"""

from crypt import methods
from shlex import join
from blinker import Namespace
from flask import Flask, render_template, request, redirect, flash, session, Response, make_response
from markupsafe import escape
from spiellogik import *
from login import login as a_login, register as a_register, psycopg2Error
import jwt
import datetime
import json
from typing import List, Tuple

from flask_socketio import SocketIO, emit, send

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
            if not gs.create_lobby(code, game_settings):
                flash("Lobby existiert bereits!", "error")
                return redirect("/")

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
        if not auth_cookie and not auth_token:
            flash('Please enter a username', 'message')
            return render_template('lobby.html', lobbyInfo=None, lobbyCode=None, players=None)
        if not auth_cookie:
            auth_cookie = auth_token
        current_lobby = gs.get_lobby_by_code(code)
        if current_lobby is None:
            return no_valid_lobby()
        decoded_auth_token = decode_token(auth_cookie)
        username = decoded_auth_token['username']
        joining_player: Player = Player(username)
        current_lobby.add_player(joining_player)
        gs.create_player(joining_player.username)
        id_0(current_lobby)

        players: list[str] = current_lobby.get_player_list()
        resp = make_response(render_template("lobby.html", lobbyInfo=current_lobby.game_settings, lobbyCode=current_lobby.code, players=players))
        resp.set_cookie('auth_token', auth_cookie)
        return resp



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
    id_0(current_lobby)

    return redirect("/")


@app.route("/lobby/<code>/start", methods=["GET"])
def start_game(code):
    auth_token = request.cookies.get('auth_token', None)
    if not auth_token:
        flash("You must be logged in", "error")
        return redirect("/")
    
    if (gs.get_game_by_id(code) != None): return redirect(f"/game/{code}") # Redirect to game page if already started

    lobby: Optional[Lobby] = gs.get_lobby_by_code(code)
    if lobby is None:
        flash("Lobby nicht gefunden", "error")
        return redirect("/")  # Check if lobby exists
    
    #if (len(lobby.get_players()) < 2): 
    #    return redirect(f"/lobby/{code}") # Not enough players

    gs.start_game(gs.get_id(code), id_2)

    game: Optional[Game] = gs.get_game_by_code(code)


    id_1(lobby)

    print("Started Game")
    return redirect(f"/game/{code}")



def write_log(data):
    pass
    #file = open("log.txt", "a")
    #file.write(str(data) + "\n")
    #file.close()


def write_send_log(data):
    pass
    #file = open("log_send.txt", "a")
    #file.write(str(data) + "\n")
    #file.close()


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
    
    return render_template("game.html", lobbyCode=code)


@app.route("/scoreboard/<code>", methods=["GET"])
def load_scoreboard(code):
    finished_game: Game = gs.get_game_by_code(code)
    players: list[Player] = finished_game.player_list
    scores: list[int] = finished_game.calculate_total_points()
    players_scores_list: List[Tuple[Player, int]] = list(zip(players, scores))
    sorted_players_scores: List[Tuple[Player, int]] = sorted(players_scores_list, key=lambda x: x[1], reverse=True)
    write_log([players, scores, players_scores_list, sorted_players_scores])
    return render_template("scoreboard.html", lobbyCode=code, playersScores=sorted_players_scores)

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



##################### Websocket

def write_socket_log(data):
    print(data)
    file = open("log_socket.txt", "a")
    file.write(str(data) + "\n")
    file.close()


def id_0(lobby: Lobby) -> None:
    """
    Send player status update
    """
    msg = {"id": 0, "players": lobby.get_player_list(), "lobby_code":lobby.code}
    write_socket_log(msg)
    socketio.emit("message", json.dumps(msg), namespace="")


def id_1(lobby: Lobby) -> None:
    """
    Start game
    """
    msg = {"id":1, "lobby_code":lobby.code}
    write_socket_log(msg)
    socketio.emit("message", json.dumps(msg), namespace="")



def id_2(lobby: Lobby, question_index: int, question: Question) -> None:
    """
    Sends the current question
    """
    msg = {"id" : 2, "question_index": question_index, "question": question.question, "answers": question.answers, "lobby_code": lobby.code}
    write_socket_log(msg)
    socketio.emit("message", json.dumps(msg), namespace="")

def id_5(lobby: Lobby) -> None:
    """
    Switch to scoreboard
    """
    msg = {"id":5, "lobby_code":lobby.code}
    write_socket_log(msg)
    socketio.emit("message", json.dumps(msg), namespace="")

@socketio.on('message')
def handle_message(data_raw):
    data = json.loads(str(data_raw)) # Convert to json

    game: Optional[Game] = gs.get_game_by_code(data["lobby_code"])
    lobby: Optional[Lobby] = gs.get_lobby_by_code(data["lobby_code"])
    
    if game is None or lobby is None: return

    if (data["id"] == 3):
        write_socket_log(data)
        print("id 3")
        if data["question_index"] != game.current_question: return
        player: Optional[Player] = gs.get_player_by_username(str(decode_token(data["auth_token"])["username"]))
        if player is None: return
        game.answer(player, data["answer"])
        write_socket_log(f"Answer from {player.username} with answer {data['answer']}")
        
        next_q: bool = game.next_question() 
        if (next_q):
            write_socket_log("Next question")


        if not next_q and game.all_answered() and game.current_question == (len(game.questions)-1):
            id_5(lobby)

    if (data["id"] == 4):
        write_socket_log(data)
        question_index = game.current_question
        question = game.questions[game.current_question]

        #msg = {"id" : 2, "question_index": question_index, "question": question.question, "answers": question.answers, "lobby_code": lobby.code}
        #write_socket_log(msg)
        #emit("message", json.dumps(msg), namespace="")
        id_2(lobby, game.current_question, game.questions[game.current_question])

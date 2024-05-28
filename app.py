from crypt import methods
from flask import Flask, render_template, request, redirect
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
        if (form.get("lobbyFormType") == "create"):
            return redirect("lobby.html", lobbyInfo = form)
        elif (form.get("lobbyFormType") == "join"):
            #return render_template("lobby.html", lobbyInfo = form)
            return redirect("/")
    elif (request.method == "POST"):
        render_template("lobby.html", )
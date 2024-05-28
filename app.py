from crypt import methods
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/lobby/<id>", methods=["GET", "POST"])
def lobby(id):
    return f"<p>Lobby {escape(id)}</p>"
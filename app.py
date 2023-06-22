from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "My super secret key" 

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def show_start():
    return render_template("base.html")

@app.route("/start")
def show_board():
    board = boggle_game.make_board()
    session["board"] = board
    return render_template("game.html", board=board)

@app.route("/submit", methods=["POST"])
def submit_word():
    word = request.json["word"]
    result = boggle_game.check_valid_word(session["board"], word)
    response = make_response(jsonify({"result": result}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


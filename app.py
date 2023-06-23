from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "My super secret key" 

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def show_start():
    session["number-of-plays"] = 0
    session["high-score"] = 0
    return render_template("base.html")

@app.route("/start")
def show_board():
    board = boggle_game.make_board()
    session["board"] = board
    return render_template("game.html")

@app.route("/submit", methods=["POST"])
def submit_word():
    word = request.json["word"]
    result = boggle_game.check_valid_word(session["board"], word)
    is_unique = word not in boggle_game.found_words
    if is_unique:
        boggle_game.found_words.append(word)
    response = make_response(jsonify({"result": result, "is-unique": is_unique}), 200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/endgame", methods=["POST"])
def endGame():
    #import pdb
   #pdb.set_trace()
    score = int(request.json["score"])
    number_of_plays = session["number-of-plays"]
    high_score = session["high-score"]
   
    if score > high_score:
        high_score = score

    
    number_of_plays += 1
    session["number-of-plays"] = number_of_plays
    session["high-score"] = high_score
    print("High Score: " + str(session['high-score']))
    session['fav-numb'] = 42
    return render_template("game.html")

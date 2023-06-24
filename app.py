from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify, make_response, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "My super duper secret key" 

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def show_start():
    """Shows homepage where user can click the start button to start the game"""
    session["number-of-plays"] = 0
    session["high-score"] = 0
    return render_template("base.html")

@app.route("/start")
def show_board():
    """Starts the game. Creates board and Displays board to the user."""
    boggle_game.clearFoundWords()  #necessary if the game has already been played
    board = boggle_game.make_board()
    session["board"] = board
    return render_template("game.html")

@app.route("/submit", methods=["POST"])
def submit_word():
    """Called when user submits a word in the provided form"""
    word = request.json["word"]
    result = boggle_game.check_valid_word(session["board"], word)
    is_unique = word not in boggle_game.found_words
    if is_unique:
        boggle_game.found_words.append(word)
    response = jsonify({"result": result, "is-unique": is_unique})
    return response

@app.route("/endgame", methods=["POST"])
def endGame():
    """Called when the timer hits 0. Submits the user's score and will update the high score 
    if appropriate. Sends back a JSON response so that the high score is updated as soon as
    the game ends. Also increments the number of plays. """
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
    #session['fav-numb'] = 42
    response = {
        "high_score": high_score,
        "number_of_plays": number_of_plays
    }
    return jsonify(response)

@app.route("/restart", methods=["POST"])
def restart():
    """Called when user clicks the restart button"""
    print("INside restart func")
    return redirect("/start")
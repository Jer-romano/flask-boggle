from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify, make_response, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "My super duper secret key" 

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def show_start():
    """Shows homepage where user can click the start button to start the game"""
    session["number_of_plays"] = 0
    session["high_score"] = 0
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
    board = session.get('board')
    if board is None:
        # Handle the case when "board" key is not present in the session
        return jsonify({"error": "'board' not found in session"})
    
    result = boggle_game.check_valid_word(board, word)
    is_unique = word not in boggle_game.found_words
    if is_unique:
        boggle_game.found_words.append(word)
    response = jsonify({"result": result, "is-unique": is_unique})
    return response


@app.route("/endgame", methods=["POST"])
def endGame():
    """Called when the timer hits 0. Submits the user's score and will update the high score 
    if appropriate. Sends back a JSON response so that the high score is updated on the DOM
     as soon as the game ends. Also increments the number of plays. """
    #import pdb
   #pdb.set_trace()
    score = int(request.json.get("score"))
    number_of_plays = session.get("number_of_plays")
    high_score = session.get("high_score")
   
    if score > high_score:
        high_score = score
        flash("New High Score!")
    number_of_plays += 1
    session["number_of_plays"] = number_of_plays
    session["high_score"] = high_score
    response = {
        "high_score": high_score,
        "number_of_plays": number_of_plays
    }
    return jsonify(response)

@app.route("/restart")
def restart():
    """Called when user clicks the restart button"""
    print("Inside restart func")
    return redirect("/start")
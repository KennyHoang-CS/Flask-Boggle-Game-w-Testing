from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "qowmdfkaqopd"

boggle_game = Boggle()

@app.route('/')
def home():
    """ Display the board. """

    # Create the board.
    board = boggle_game.make_board()

    # Save the board to session.
    session['board'] = board

    # Get high score from session.
    highscore = session.get('highscore', 0)

    # Get number of plays.
    num_plays = session.get('num_plays', 0)

    return render_template('index.html', board=board, highscore=highscore, num_plays=num_plays)


@app.route('/check-word')
def validate_word():
    """ Is the word in dictionary? """

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route('/post-score', methods=["POST"])
def post_score():
    """ Receive score, update num_plays, update high score. """

    score = request.json['score']
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)

    # Update the session.
    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newRecord=score > highscore)

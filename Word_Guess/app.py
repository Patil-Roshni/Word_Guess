from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "pink_secret_key"

WORD_LIST = ["python", "java", "javascript", "ruby", "php", "html", "css", "rust", "golang"]

def get_display_word(word, guessed):
    return " ".join([l if l in guessed else "_" for l in word])

@app.route('/')
def index():
    # Setup new game
    word = random.choice(WORD_LIST)
    session['word'] = word
    session['guessed'] = []
    session['attempts'] = 6
    return render_template('index.html', display=get_display_word(word, []))

@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    letter = data.get('letter', '').lower()
    word = session.get('word')
    guessed = session.get('guessed', [])
    attempts = session.get('attempts', 6)

    if letter and letter not in guessed:
        guessed.append(letter)
        if letter not in word:
            attempts -= 1
    
    session['guessed'] = guessed
    session['attempts'] = attempts

    display = get_display_word(word, guessed)
    win = "_" not in display
    game_over = attempts <= 0

    return jsonify({
        "display": display,
        "attempts": attempts,
        "used": ", ".join(guessed),
        "win": win,
        "game_over": game_over,
        "correct_word": word if game_over else ""
    })

@app.route('/reset', methods=['POST'])
def reset():
    word = random.choice(WORD_LIST)
    session['word'] = word
    session['guessed'] = []
    session['attempts'] = 6
    return jsonify({
        "display": get_display_word(word, []),
        "attempts": 6,
        "used": ""
    })

if __name__ == '__main__':
    app.run(debug=True)
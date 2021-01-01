from flask import Flask, send_from_directory, render_template, redirect, url_for
import random
import json

app = Flask(__name__)
game = False


@app.route('/')
def first():
    return render_template('first.html')


@app.route('/app')
def application():
    # return send_from_directory('client/public', 'index.html')
    return render_template('index.html', gamestatus=game)


@app.route('/app/<path:path>')
def base(path):
    return send_from_directory('client/public', path)


@app.route('/rand')
def rand():
    return str(random.randint(0, 100))


@app.route('/start-game', methods=['POST', 'GET'])
def start():
    global game
    game = True
    return redirect(url_for('application'))


@app.route('/game-status')
def game_status():
    return json.dumps({'gameStatus': game})


@app.route('/vue')
def vue():
    return render_template('vue.html', gamestatus=game)

if __name__ == '__main__':
    app.run()

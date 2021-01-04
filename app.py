from flask import Flask, send_from_directory, render_template, redirect, url_for, request
import random
import json

app = Flask(__name__)
gameRunning = False
players = []


@app.route('/')
def prepare():
    return redirect(url_for('application'))


@app.route('/players', methods=['GET', 'POST'])
def players_route():
    if request.method == 'POST':
        players.append(request.json)
    return json.dumps({'players': players})


@app.route('/app')
def application():
    # return send_from_directory('client/public', 'index.html')
    return render_template('index.html', gameRunning=gameRunning)


@app.route('/app/<path:path>')
def base(path):
    return send_from_directory('client/public', path)


@app.route('/rand')
def rand():
    return str(random.randint(0, 100))


@app.route('/start', methods=['POST'])
def start_game():
    global gameRunning
    gameRunning = True
    return json.dumps({'gameRunning': gameRunning})


@app.route('/game')
def game_running():
    return json.dumps({'gameRunning': gameRunning})


if __name__ == '__main__':
    app.run()

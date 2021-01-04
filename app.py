from flask import Flask, send_from_directory, render_template, redirect, url_for, request
import random
import json

app = Flask(__name__)
game = False
players = []

@app.route('/')
def prepare():
    return render_template('index.html')
    # return render_template('prepare.html')


@app.route('/addPlayer', methods=['GET', 'POST'])
def players_route():
    if request.method == 'POST':
        players.append(request.json)
    return json.dumps({'players': players})


@app.route('/app')
def application():
    # return send_from_directory('client/public', 'index.html')
    # return render_template('index.html')
    return render_template('prepare.html')


@app.route('/app/<path:path>')
def base(path):
    return send_from_directory('client/public', path)


@app.route('/rand')
def rand():
    return str(random.randint(0, 100))


@app.route('/start', methods=['POST', 'GET'])
def start():
    global game
    game = True
    return redirect(url_for('game_status'))


@app.route('/game-status')
def game_status():
    return json.dumps({'gameStatus': game})


if __name__ == '__main__':
    app.run()

from flask import Flask, redirect, url_for, request, render_template, send_from_directory, Blueprint
from flask_socketio import SocketIO
import random
import json
import uuid

app = Flask(__name__)
client = Blueprint('client', __name__, template_folder='templates')
api = Blueprint('api', __name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

players = []
activePlayer = -1
gameRunning = False


@app.route('/')
def application():
    # return redirect(url_for('client.application'))
    return render_template('index.html', gameRunning=gameRunning, players=json.dumps(players))


# @client.route('/')
# def application():
    # return send_from_directory('client/public', 'index.html')
    # return render_template('index.html', gameRunning=gameRunning)


@client.route('/<path:path>')
def base(path):
    return send_from_directory('client/public', path)


@api.route('/rand')
def rand():
    return str(random.randint(0, 100))


@api.route('/start', methods=['POST'])
def start_game():
    global gameRunning
    global activePlayer
    if len(players) > 0:
        gameRunning = True
        activePlayer = random.randint(0, len(players))
        players[activePlayer]['active'] = True
    send_players()
    return json.dumps({'gameRunning': gameRunning})


@api.route('/next-player', methods=['POST'])
def next_player():
    global activePlayer
    players[activePlayer]['active'] = False
    activePlayer += 1
    if activePlayer >= len(players):
        activePlayer = 0
    players[activePlayer]['active'] = True
    send_players()
    return json.dumps({'gameRunning': gameRunning})


app.register_blueprint(client, url_prefix='/app')
app.register_blueprint(api, url_prefix='/api')


@socketio.on('message')
def handle_event(data):
    print('Message received: ' + str(data))
    socketio.emit('response', data)


def send_players():
    print('Players sent: ' + str(players))
    socketio.emit('players', json.dumps(players))


@socketio.on('addPlayer')
def add_player(data):
    print('Player received to ADD: ' + str(data))
    entry = {'uuid': str(uuid.uuid4()),
             'name': data['name'],
             'points': 501,
             'active': False}
    players.append(entry)
    print('Player added: ' + str(entry))
    send_players()


@socketio.on('removePlayer')
def remove_player(data):
    print('Player received to REMOVE: ' + str(data))
    players.remove(data)
    send_players()


if __name__ == '__main__':
    socketio.run(app, debug=True, port=3000)

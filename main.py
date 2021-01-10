from flask import Flask, Response, render_template, send_from_directory, Blueprint
from flask_socketio import SocketIO
import random
import json
import uuid
import datetime

app = Flask(__name__)
client = Blueprint('client', __name__, template_folder='templates')
api = Blueprint('api', __name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

PLAYERS = []
SERVER_STATE = 'New Game'
GAMEMODE = '501'
DARTS = [0, 0, 0]
DTObj = open('static/darts.json')
DART_TARGETS = json.load(DTObj)

activePlayer = -1
copyright_year = datetime.datetime.now().year


@app.route('/')
def application():
    return render_template('index.html',
                           SERVER_STATE=SERVER_STATE,
                           PLAYERS=json.dumps(PLAYERS),
                           GAMEMODE=GAMEMODE,
                           DARTS=DARTS,
                           DART_TARGETS=DART_TARGETS,
                           copyright_year=copyright_year)


@client.route('/<path:path>')
def base(path):
    return send_from_directory('client/public', path)


@api.route('/start', methods=['POST'])
def start_game():
    global activePlayer
    global SERVER_STATE
    if len(PLAYERS) == 0:
        return Response(status=400)
    SERVER_STATE = 'Started'
    random.shuffle(PLAYERS)
    activePlayer = 0
    PLAYERS[activePlayer]['active'] = True

    for player in PLAYERS:
        if GAMEMODE == '501':
            player['points'] = 501
        elif GAMEMODE == '301':
            player['points'] = 301

    send_players()
    send_server_state()
    return Response(status=200)


@api.route('/next-player', methods=['POST'])
def next_player():
    global activePlayer
    global DARTS
    PLAYERS[activePlayer]['points'] -= DART_TARGETS[DARTS[0]]['value'] + DART_TARGETS[DARTS[1]]['value'] + DART_TARGETS[DARTS[2]]['value']
    PLAYERS[activePlayer]['active'] = False
    activePlayer += 1
    if activePlayer >= len(PLAYERS):
        activePlayer = 0
    PLAYERS[activePlayer]['active'] = True
    DARTS = [0, 0, 0]
    socketio.emit('darts', json.dumps(DARTS))
    print('Darts sent: ' + str(json.dumps(DARTS)))
    send_players()
    return Response(status=200)


@api.route('/reset', methods=['POST'])
def reset():
    global PLAYERS
    global SERVER_STATE
    global GAMEMODE
    global DARTS
    PLAYERS = []
    SERVER_STATE = 'New Game'
    GAMEMODE = '501'
    DARTS = [0, 0, 0]
    socketio.emit('darts', json.dumps(DARTS))
    print('Darts sent: ' + str(json.dumps(DARTS)))
    socketio.emit('gamemode', json.dumps(GAMEMODE))
    print('Game Mode sent: ' + str(json.dumps(GAMEMODE)))
    send_players()
    send_server_state()
    return Response(status=200)


app.register_blueprint(client, url_prefix='/app')
app.register_blueprint(api, url_prefix='/api')


def send_players():
    print('Players sent: ' + str(json.dumps(PLAYERS)))
    socketio.emit('players', json.dumps(PLAYERS))


def send_server_state():
    print('SERVER_STATE sent: ' + SERVER_STATE)
    socketio.emit('SERVER_STATE', json.dumps(SERVER_STATE))


@socketio.on('addPlayer')
def add_player(data):
    print('Player received to ADD: ' + str(data))
    entry = {'uuid': str(uuid.uuid4()),
             'name': json.loads(data)['name'],
             # 'points': 501,
             'active': False}
    PLAYERS.append(entry)
    print('Player added: ' + str(json.dumps(entry)))
    send_players()


@socketio.on('removePlayer')
def remove_player(data):
    print('Player received to REMOVE: ' + str(data))
    PLAYERS.remove(json.loads(data))
    send_players()


@socketio.on('setGameMode')
def set_game_mode(data):
    print('Game Mode received: ' + str(data))
    global GAMEMODE
    GAMEMODE = json.loads(data)['gamemode']
    socketio.emit('gamemode', json.dumps(GAMEMODE))
    print('Game Mode sent: ' + str(json.dumps(GAMEMODE)))


@socketio.on('setDarts')
def set_darts(data):
    print('Darts received: ' + str(data))
    global DARTS
    DARTS = json.loads(data)
    socketio.emit('darts', json.dumps(DARTS))
    print('Darts sent: ' + str(json.dumps(DARTS)))


if __name__ == '__main__':
    socketio.run(app, debug=True, port=3000, host='0.0.0.0')

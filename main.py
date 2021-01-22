from flask import Flask, Response, render_template, send_from_directory, Blueprint
from flask_socketio import SocketIO
import random
import json
import uuid
import datetime
import re
import socket

app = Flask(__name__)
client = Blueprint('client', __name__, template_folder='templates')
api = Blueprint('api', __name__, template_folder='templates')
app.config['SECRET_KEY'] = 'notsosecret!'
socketio = SocketIO(app)
ip = socket.gethostbyname(socket.gethostname())
port = 3000


# -------------------------------
# Init
# -------------------------------

PLAYERS = []
SERVER_STATE = 'New Game'
GAMEMODE = '501'
CLIENT_DARTS = [0, 0, 0]
DTObj = open('static/darts.json')
DTCOObj = open('static/dart-checkout.json')
DART_TARGETS = json.load(DTObj)
DART_CHECKOUT = json.load(DTCOObj)
LAST_SENSOR_DARTS = []
activePlayer = -1
copyright_year = datetime.datetime.now().year


# -------------------------------
# APP Routes
# -------------------------------

@app.route('/')
def application():
    return render_template('index.html',
                           SERVER_STATE=SERVER_STATE,
                           PLAYERS=json.dumps(PLAYERS),
                           GAMEMODE=GAMEMODE,
                           DARTS=CLIENT_DARTS,
                           DART_TARGETS=DART_TARGETS,
                           DART_CHECKOUT=DART_CHECKOUT,
                           LAST_SENSOR_DARTS=LAST_SENSOR_DARTS,
                           copyright_year=copyright_year,
                           ip=ip,
                           port=port)


@client.route('/<path:path>')
def base(path):
    return send_from_directory('client/public', path)


# -------------------------------
# API Routes
# -------------------------------

def darts_over():
    global PLAYERS
    global activePlayer
    PLAYERS[activePlayer]['turns'].append([0, 0, 0])
    reset_and_send_darts()
    PLAYERS[activePlayer]['active'] = False
    activePlayer += 1
    if activePlayer >= len(PLAYERS):
        activePlayer = 0
    PLAYERS[activePlayer]['active'] = True
    # send_players()


def get_points(player):
    return player['points']


def end_game():
    global SERVER_STATE
    global PLAYERS
    PLAYERS.sort(key=get_points)
    for player in PLAYERS:
        player['active'] = False
    # send_players()
    SERVER_STATE = 'End Game'
    send_server_state()
    socketio.emit('sensor-end-game')


def confirm_new_points(new_points, combined_darts):
    global activePlayer
    global SERVER_STATE
    global PLAYERS

    if new_points > 0:
        # Normal
        PLAYERS[activePlayer]['points'] = new_points
        PLAYERS[activePlayer]['turns'].append([combined_darts[0], combined_darts[1], combined_darts[2]])

        PLAYERS[activePlayer]['active'] = False
        activePlayer += 1
        if activePlayer >= len(PLAYERS):
            activePlayer = 0
        PLAYERS[activePlayer]['active'] = True
        # send_players()
        reset_and_send_darts()

    elif new_points == 0:
        # Exact

        # Check win
        check = combined_darts.copy()
        for throw in check:
            if DART_TARGETS[check[-1]]['value'] == 0:
                check.pop()
        if DART_TARGETS[check[-1]]['type'] == 'double':
            PLAYERS[activePlayer]['points'] = new_points
            PLAYERS[activePlayer]['turns'].append([combined_darts[0], combined_darts[1], combined_darts[2]])
            end_game()
        else:
            darts_over()

    else:
        # Over
        darts_over()

    send_players()


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

    reset_and_send_darts()
    send_players()
    send_server_state()
    socketio.emit('sensor-start-game')
    return Response(status=200)


@api.route('/confirm-turn', methods=['POST'])
def confirm_turn():
    global CLIENT_DARTS
    global PLAYERS
    global activePlayer

    combined_darts = [0, 0, 0]
    for i in range(len(LAST_SENSOR_DARTS)):
        if LAST_SENSOR_DARTS[i] is not None:
            combined_darts[i] = (LAST_SENSOR_DARTS[i][2])
    for i in range(3):
        if DART_TARGETS[CLIENT_DARTS[i]]['type'] != "none":
            combined_darts[i] = (CLIENT_DARTS[i])

    new_points = PLAYERS[activePlayer]['points'] \
                 - DART_TARGETS[combined_darts[0]]['value'] \
                 - DART_TARGETS[combined_darts[1]]['value'] \
                 - DART_TARGETS[combined_darts[2]]['value']

    if new_points > 0:
        if not (DART_TARGETS[combined_darts[0]]['name'] == "" or DART_TARGETS[combined_darts[1]]['name'] == ""
                or DART_TARGETS[combined_darts[2]]['name'] == ""):
            confirm_new_points(new_points, combined_darts)
            socketio.emit('sensor-start-game')
            return Response(status=200)
        else:
            return "No enough darts confirmed", 400

    else:
        confirm_new_points(new_points, combined_darts)
        socketio.emit('sensor-start-game')
        return Response(status=200)


@api.route('/reset', methods=['POST'])
def reset():
    global PLAYERS
    global SERVER_STATE
    global GAMEMODE
    global CLIENT_DARTS
    PLAYERS = []
    SERVER_STATE = 'New Game'
    GAMEMODE = '501'
    reset_and_send_darts()
    socketio.emit('gamemode', json.dumps(GAMEMODE))
    print('Game Mode sent: ' + str(json.dumps(GAMEMODE)))
    send_players()
    send_server_state()
    socketio.emit('sensor-end-game')
    return Response(status=200)


@api.route('/next-leg', methods=['POST'])
def next_leg():
    global PLAYERS
    global SERVER_STATE
    global GAMEMODE
    global CLIENT_DARTS
    global activePlayer
    for player in PLAYERS:
        if GAMEMODE == '501':
            player['points'] = 501
        elif GAMEMODE == '301':
            player['points'] = 301
        player['turns'] = []
    random.shuffle(PLAYERS)
    activePlayer = 0
    PLAYERS[activePlayer]['active'] = True
    send_players()
    SERVER_STATE = 'Started'
    send_server_state()
    reset_and_send_darts()
    socketio.emit('sensor-start-game')
    return Response(status=200)


# -------------------------------
# SocketIO Routes
# -------------------------------

def send_players():
    print('Players sent: ' + str(json.dumps(PLAYERS)))
    socketio.emit('players', json.dumps(PLAYERS))


def send_server_state():
    print('SERVER_STATE sent: ' + SERVER_STATE)
    socketio.emit('SERVER_STATE', json.dumps(SERVER_STATE))


def reset_and_send_darts():
    global CLIENT_DARTS, LAST_SENSOR_DARTS
    CLIENT_DARTS = [0, 0, 0]
    LAST_SENSOR_DARTS = []
    socketio.emit('sensorDarts', json.dumps(LAST_SENSOR_DARTS))
    socketio.emit('darts', json.dumps(CLIENT_DARTS))
    print('Darts sent: ' + str(json.dumps(CLIENT_DARTS)))


@socketio.on('addPlayer')
def add_player(data):
    ldata = json.loads(data)
    if ldata['name']:
        if not ldata['name'] == "" and re.search("[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð]+", ldata["name"]):
            print('Player received to ADD: ' + str(ldata))
            entry = {'uuid': str(uuid.uuid4()),
                     'name': ldata['name'],
                     # 'points': 501,
                     'checkout': True,
                     'active': False,
                     'turns': []}
            PLAYERS.append(entry)
            print('Player added: ' + str(json.dumps(entry)))
            send_players()


@socketio.on('removePlayer')
def remove_player(data):
    ldata = json.loads(data)
    # if ldata['uuid'] and ldata['name'] and ldata['active'] and ldata['turns']:
    print('Player received to REMOVE: ' + str(ldata))
    PLAYERS.remove(ldata)
    send_players()


@socketio.on('togglePlayerCheckout')
def toggle_player_checkout(data):
    ldata = json.loads(data)
    print('Player received to TOGGLE CHECKOUT: ' + str(ldata))
    player = next(i for i, p in enumerate(PLAYERS) if p['uuid'] == ldata['uuid'])
    PLAYERS[player]['checkout'] = not PLAYERS[player]['checkout']
    send_players()


@socketio.on('setGameMode')
def set_game_mode(data):
    # TODO: Check for valid gamemode
    print('Game Mode received: ' + str(data))
    global GAMEMODE
    GAMEMODE = json.loads(data)['gamemode']
    socketio.emit('gamemode', json.dumps(GAMEMODE))
    print('Game Mode sent: ' + str(json.dumps(GAMEMODE)))


@socketio.on('setDarts')
def set_darts(data):
    ldata = json.loads(data)
    # TODO: Check for valid darts
    if len(ldata) == 3 and type(ldata[0]) is int and type(ldata[1]) is int and type(ldata[2]) is int :
        print('Darts received: ' + str(ldata))
        global CLIENT_DARTS
        CLIENT_DARTS = ldata
        socketio.emit('darts', json.dumps(CLIENT_DARTS))
        print('Darts sent: ' + str(json.dumps(CLIENT_DARTS)))


@socketio.on('sensorDarts')
def sensor_darts(data):
    ldata = json.loads(data)
    global LAST_SENSOR_DARTS
    LAST_SENSOR_DARTS = ldata
    socketio.emit('sensorDarts', json.dumps(ldata))


app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(client, url_prefix='/app')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=port, host='0.0.0.0')

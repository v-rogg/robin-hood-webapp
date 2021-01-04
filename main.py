from flask import Flask, redirect, url_for, request, render_template, send_from_directory, Blueprint
from flask_socketio import SocketIO
import random
import json

app = Flask(__name__)
client = Blueprint('client', __name__, template_folder='templates')
api = Blueprint('api', __name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

players = []
gameRunning = False


@app.route('/')
def application():
    # return redirect(url_for('client.application'))
    return render_template('index.html', gameRunning=gameRunning, players=players)


# @client.route('/')
# def application():
    # return send_from_directory('client/public', 'index.html')
    # return render_template('index.html', gameRunning=gameRunning)


@client.route('/<path:path>')
def base(path):
    return send_from_directory('client/public', path)


@api.route('/players', methods=['GET', 'POST'])
def players_api():
    if request.method == 'POST' and not gameRunning:
        players.append(request.json)
        socketio.emit('response', json.dumps({'players': players}))
    return json.dumps({'players': players})


@api.route('/rand')
def rand():
    return str(random.randint(0, 100))


@api.route('/start', methods=['POST'])
def start_game():
    global gameRunning
    gameRunning = True
    return json.dumps({'gameRunning': gameRunning})


@api.route('/game')
def game_running():
    return json.dumps({'gameRunning': gameRunning})


app.register_blueprint(client, url_prefix='/app')
app.register_blueprint(api, url_prefix='/api')


@socketio.on('message')
def handle_event(data):
    print('Message received: ' + str(data))
    socketio.emit('response', data)


@socketio.on('addPlayer')
def add_player(data):
    print('Player received: ' + str(data))
    players.append(data)
    print('Players sent: ' + str(players))
    socketio.emit('players', players)


if __name__ == '__main__':
    # app.run()
    socketio.run(app, debug=True, port=3000)

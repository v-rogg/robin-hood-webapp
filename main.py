from flask import Flask, redirect, url_for, request, render_template, send_from_directory, Blueprint
import random
import json

app = Flask(__name__)
client = Blueprint('client', __name__, template_folder='templates')
api = Blueprint('api', __name__, template_folder='templates')

players = []
gameRunning = False


@app.route('/')
def prepare():
    return redirect(url_for('client.application'))


@client.route('/')
def application():
    # return send_from_directory('client/public', 'index.html')
    return render_template('index.html', gameRunning=gameRunning)


@client.route('/<path:path>')
def base(path):
    return send_from_directory('client/public', path)


@api.route('/players', methods=['GET', 'POST'])
def players_route():
    if request.method == 'POST':
        players.append(request.json)
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


if __name__ == '__main__':
    app.run()

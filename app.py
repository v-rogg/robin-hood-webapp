from flask import Flask, render_template
import json

app = Flask(__name__)

weather = True


@app.route('/')
@app.route('/<name>')
def base(name=None):
    if name:
        name = name.title()

    return render_template('hello.html', name=name, weather=weather)


@app.route('/change-weather', methods=['POST'])
def change():
    global weather
    weather = not weather
    if weather:
        return json.dumps({'msg': "The weather is sunny outside :) nice"})
    else:
        return json.dumps({'msg': "The weather is cloudy inside. Lol wut?"})


if __name__ == '__main__':
    app.run()

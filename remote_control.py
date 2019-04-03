'''Web server that is central to running and training the autonomous car.
Implements the remote control for controlling the car, handles requests
for images on the remote, and allows both recording and auto mode to be
toggled.'''

from flask import Flask, render_template, Response
from time import sleep
from keras.models import load_model

from car import Car, PWMCar
from camera import Camera
from recorder import Recorder
from autodriver import AutoDriver

# Defines the web app, car, camera, recorder, model, and autodriver

app = Flask(__name__)

car = PWMCar(forward = 18, backward = 23, right = 14, left = 15, speed = 0.8)

camera = Camera(resolution = 64, framerate = 30)

recorder = Recorder(car = car, camera = camera, interval = 0.05)

model = load_model('models/modelA6')

model._make_predict_function() # Necessary for model to run

autodriver = AutoDriver(car = car, camera = camera, interval = 0.00, model = model)

# Shortcuts to convert the command path to the function
commands = {'left': car.left,
            'right': car.right,
            'forward': car.forward,
            'backward': car.backward,
            'stop': car.stop,
            'straight': car.straight}

@app.route('/')
def index():
    '''Main path where the remote is accessed.'''

    return render_template('index.html')

@app.route('/image')
def image():
    '''Sends raw jpeg binary for rendering on the remote.'''

    resp = Response(camera.binary(), mimetype = 'image.jpeg')

    resp.headers['Cache-Control'] = 'no-cache'

    return resp

@app.route('/record')
def record():
    '''Toggles recording mode for the recorder.'''

    print('Recording was toggled')
    recorder.toggle_record()
    return ('', 204)

@app.route('/auto')
def auto():
    '''Toggles autonomous mode for the car.'''

    print('Automatic mode was toggled')
    autodriver.toggle_auto()
    return ('', 204)

@app.route('/drive/<cmd>')
def cmd(cmd):
    '''Handles requests from the buttons to move the car correctly.'''

    commands[cmd]()
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)

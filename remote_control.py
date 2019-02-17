from flask import Flask, render_template, Response
from time import sleep
from car import Car, PWMCar
from camera import Camera
from recorder import Recorder

app = Flask(__name__)

car = PWMCar(forward = 18, backward = 23, right = 14, left = 15, speed = 1)

camera = Camera(resolution = 64, framerate = 30)

recorder = Recorder(car = car, camera = camera, interval = 0.1)

commands = {'left': car.left, 
            'right': car.right, 
            'forward': car.forward, 
            'backward': car.backward, 
            'stop': car.stop, 
            'straight': car.straight}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def image():
    resp = Response(camera.binary(), mimetype = 'image.jpeg')

    resp.headers['Cache-Control'] = 'no-cache'

    return resp

@app.route('/record')
def record():
    print('Recording was toggled')
    recorder.toggle_record()
    return ('', 204)

@app.route('/drive/<cmd>')
def cmd(cmd):
    commands[cmd]()
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)

'''Defines the class AutoDriver, which is responsible for using
the machine learning model to make an intelligent decision
about the direction the car should drive.'''

import numpy as np

from time import sleep
from threading import Thread
from datetime import datetime

from process import prep_images, reduce_dim


class AutoDriver:
    '''Uses a model to decide which direction to steer the car'''

    def __init__(self, car, camera, model, interval):
        '''Defines the drivers properties, including the car it
        can control, the camera it has access to, the model it
        relies on to make the decision, and the time between
        decisions being made. Also begins the main background thread.'''

        self.car = car
        self.camera = camera
        self.model = model
        self.interval = interval
        self.auto = False

        thread = Thread(target = self.run)
        thread.daemon = True

        thread.start()

        print('Auto Driver Active')

    def run(self):
        '''The primary background thread, that always is running. If auto mode
        is activated, then an image from the camera will be fed into the model,
        and the car will be steered in the appropriate direction'''

        target_names = ['Left', 'Right', 'Straight']

        while True:
            if self.auto:
                image = prep_images(reduce_dim([self.camera.array()], 4))

                decision = np.argmax(self.model.predict(image)[0])

                if decision == 0:
                    self.car.left()
                elif decision == 1:
                    self.car.right()
                else:
                    self.car.straight()

            sleep(self.interval)

    def toggle_auto(self):
        '''Toggles auto mode on and off.'''

        self.auto = not self.auto
        print('Auto status is ' + str(self.auto))

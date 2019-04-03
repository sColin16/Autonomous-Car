'''Defines the Recorder class, which is responsible for recording the training
data while the car is in recording mode. Runs in a background thread.'''

import numpy as np

from time import sleep
from threading import Thread
from datetime import datetime


class Recorder:
    '''Responsible for capturing the images the car sees as it is being driven.
    performs this task on a background thread so that Flask can run too'''

    def __init__(self, car, camera, interval):
        '''Defines the properties of the car, including the car whose state
        it will record, the camera that it will get images from, and the
        time it waits in between capturing images'''

        self.car = car # Allows the recorder to track the state of the car
        self.camera = camera
        self.interval = interval
        self.recording = False

        self.save_queue = [] # Saved to a file after recording stopped

        thread = Thread(target = self.run)
        thread.daemon = True # stops the thread after the main program stops

        thread.start()

        print('Recorder Active')

    def run(self):
        '''The primary background thread for the recorder, which is always running.
        When recording mdoe is on, the recorder will pair the image from the camera
        with the label from the car's steering status, and append it to an array.
        When recording mode is toggled, the array of images will be saved'''

        while True:
            drive_status, steer_status = self.car.get_status()

            if drive_status == 'forward' and self.recording:
                image = self.camera.array()
                label = self.label_to_number(steer_status)

                self.save_queue.append((image, label))

                print('Snapped a picture')

            elif not self.recording and len(self.save_queue) != 0:
                self.save()

            sleep(self.interval)

    def toggle_record(self):
        '''Toggles recording mode on and off'''

        self.recording = not self.recording
        print('Recording status is ' + str(self.recording))

    def label_to_number(self, label):
        '''Converts the steer status string to a number, for formatting purposes'''

        if label == 'left':
            return 0
        elif label == 'right':
            return 1
        else:
            return 2

    def save(self):
        '''Saves the current queue of images as the timestamp, then clears the queue.'''

        timestamp = self.timestamp()

        np.save('images/' + timestamp, self.save_queue)
        print('Saved images as ' + timestamp + ".npy")

        self.save_queue = []

    def timestamp(self):
        '''Simple function that defines what part of the timestamp are used
        when the file name is saved. Makes the name easy to change.'''

        return str(datetime.now()) # Just the default, nice and simple

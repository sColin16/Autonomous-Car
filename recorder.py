import numpy as np

from time import sleep
from threading import Thread
from datetime import datetime


class Recorder:
    '''Responsible for capturing the images the car sees as it is being driven.
    performs this task on a background thread so that Flask can run too'''
    
    def __init__(self, car, camera, interval):
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
        self.recording = not self.recording
        print('Recording status is ' + str(self.recording))

    def label_to_number(self, label):
        if label == 'left':
            return 0
        elif label == 'right':
            return 1
        else:
            return 2

    def save(self):
        timestamp = self.timestamp()

        np.save('images/' + timestamp, self.save_queue)
        print('Saved images as ' + timestamp + ".npy")

        self.save_queue = []        

    def timestamp(self):
        return str(datetime.now()) # Easy to change if needed

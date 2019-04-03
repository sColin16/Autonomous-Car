'''Defines the Camera class, which provides methods for other systems to
obtain pictures from the camera. Relies on a generator to return such images'''

from time import sleep
from io import BytesIO
from PIL import Image

import picamera
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import threading

class Camera:
    '''A wrapper for the picamera PiCamera class, which allows images to be
    streamed from the camera like a generator'''

    def __init__(self, resolution, framerate):
        self.frame = self.frame_gen()
        self.resolution = resolution
        self.framerate = framerate
        self.lock = threading.Lock()

    def frame_gen(self):
        '''Frames are captured from the camera in this generator. The resolution
        and framerate are set, and the camera takes black and white images.'''

        with picamera.PiCamera() as camera:
            camera.resolution = (self.resolution, self.resolution)
            camera.framerate = self.framerate
            camera.color_effects = (128, 128) # Makes the output black and white

            sleep(1) # Camera warm-up time

            stream = BytesIO()

            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                stream.seek(0)

                yield stream.read()

                stream.seek(0)
                stream.truncate()

    def binary(self):
        '''Returns the binary jpeg information from the last camera frame.
        The jpeg data is used to display an image on the remote'''

        with self.lock: # Locking the thread prevents multiple systems from accessing the camera at once
            return next(self.frame)

    def array(self):
        '''Returns the raw array of pixel values from the last camera frame.
        This array is used by the model to determine the steering direction'''

        binary = self.binary()

        pil = Image.open(BytesIO(binary))
        arr = np.asarray(pil) # Converts the jpeg image format to a raw array format

        return arr[:,:,0] # Only return one of the black and white color chanels

# These functions are for testing purposes:

def reduce_dim(arr, factor):
    '''Reduces the dimensions of a 2D numpy array image by slicing the array with
    a step parameter. To cut from 64x64 to 32x32 use a factor of 2'''

    return arr[::factor, ::factor]

def preview_arr(arr):
    '''Opens a preview of an array in matplotlib'''

    plt.imshow(arr, cmap = 'gray', interpolation = 'nearest')
    plt.show()

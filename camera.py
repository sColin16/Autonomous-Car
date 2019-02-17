from time import sleep
from io import BytesIO
from PIL import Image
from threadsafe import threadsafe_generator

import picamera
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Camera:
    '''A wrapper for the picamera PiCamera class, which allows images to be
    streamed from the camera like a generator'''

    def __init__(self, resolution, framerate):
        self.frame = self.frame_gen()
        self.resolution = resolution
        self.framerate = framerate

    @threadsafe_generator
    def frame_gen(self):
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
        return next(self.frame)

    def array(self):
        binary = self.binary()

        pil = Image.open(BytesIO(binary))
        arr = np.asarray(pil)

        return arr[:,:,0] # Only return one of the black and white color chanels

def reduce_dim(arr, factor):
    '''Reduces the dimensions of a 2D numpy array image by slicing the array with
    a step parameter. To cut from 64x64 to 32x32 use a factor of 2'''

    return arr[::factor, ::factor]

def preview_arr(arr):
    '''Opens a preview of an array in matplotlib'''

    plt.imshow(arr, camp = 'gray', interpolation = 'nearest')
    plt.show()

'''Contains functions that process data prior to training and predicting.
This file is run to make all the necessary datasets for training.'''

import os
import numpy as np

from keras.utils import to_categorical

INPUTDIR = 'images'
OUTPUTDIR = 'datasets'
SCALES = [1, 2, 4]

def combine(directory):
    '''Combines all the data from a directory into one big array'''

    final = None

    for filename in os.listdir(directory):
        if filename.endswith('.npy'):
            if final is None:
                final = np.load(directory + '/' + filename)
            else:
                final = np.vstack((final, np.load(directory + '/' + filename)))

    return final

def get_images(dataset):
    '''Returns all the images from a dataset'''

    return np.array([image for image in dataset[:, 0]])

def get_labels(dataset):
    '''Returns all the labels from a dataset'''

    return dataset[:, 1]

def reduce_dim(images, factor):
    '''Converts images to lower quality by slicing out parts of the image.
    Use a factor of 2 to got from 64x64 to 32x32'''

    return np.array([image[::factor, ::factor] for image in images])

def prep_images(images):
    '''Reshapes an array of images, scales to between 0 and 1
    Prepares the images for use with keras'''

    dim = images.shape[1]

    images = images.reshape(-1, dim, dim, 1)
    images = images/255

    return images

def prep_labels(labels):
    '''Uses one-hot encoding to set up labels for training.
    This is the format that keras wants them in for training.'''

    return to_categorical(labels)

def make_dataset(inputdir, outputdir, scales):
    '''Does all the steps at once. Combines the images from a directory,
    seperates the data into images and labels, creates different resolution
    copy of the images, and then saves the images and labels.'''

    combined = combine(inputdir)

    images = get_images(combined)
    labels = get_labels(combined)

    for scale in scales:
        image_data = reduce_dim(images, scale)
        print(image_data.shape)
        np.save(outputdir + '/image' + str(int(64/scale)), image_data)

    np.save(outputdir + '/labels', labels)
    print(labels.shape)

def main():
    make_dataset(INPUTDIR, OUTPUTDIR, SCALES)

if __name__ == '__main__':
    main()

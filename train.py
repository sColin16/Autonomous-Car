'''Contains functions for training models, and visualizing information
and how the training went. This function is run to train and save a model.'''

import keras
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.callbacks import ModelCheckpoint

from sklearn.metrics import classification_report

from models import modelA, modelB, modelC, modelD, modelE
from process import prep_images, prep_labels

BATCH_SIZE = 64
EPOCHS = 20
VAL_SPLIT = 0.1

IMAGEPATH = 'datasets/image16.npy'
LABELPATH = 'datasets/labels.npy'

MODEL = modelA()
OUTPUT = 'models/modelA7'

IMAGES = prep_images(np.load(IMAGEPATH))
LABELS = prep_labels(np.load(LABELPATH))

def train(model, images, labels, output):
    callback = ModelCheckpoint(filepath = output, monitor = 'val_acc', verbose = 1, save_best_only = True)

    model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(), metrics=['accuracy'])

    return model.fit(images, labels, batch_size = BATCH_SIZE, epochs = EPOCHS, validation_split = VAL_SPLIT, callbacks = [callback])

def report(history, model):
    '''Gives a variety of information about the model\'s training. Adapted from Aditya Sharma:
    https://www.datacamp.com/community/tutorials/convolutional-neural-networks-python'''

    accuracy = history.history['acc']
    val_accuracy = history.history['val_acc']
    epochs = range(len(accuracy))
    plt.plot(epochs, accuracy, 'b', label='Training accuracy')
    plt.plot(epochs, val_accuracy, 'r', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.show()

    predicted_classes = model.predict(IMAGES)
    predicted_classes = np.argmax(np.round(predicted_classes),axis=1)

    raw_labels = np.load(LABELPATH)

    target_names = ['Left', 'Right', 'Straight']

    print('Displaying Correctly Identified Labels:')
    correct = np.where(predicted_classes == raw_labels)[0]
    for i, correct in enumerate(np.random.choice(correct, 9)):
        plt.subplot(3, 3, i + 1)
        plt.imshow(IMAGES[correct].reshape(16, 16), cmap = 'gray', interpolation = 'none')
        plt.title("P: {}, L: {}".format(target_names[predicted_classes[correct]], target_names[raw_labels[correct]]))
        plt.tight_layout()

    plt.show()

    print('Displaying Incorrectly Identified Labels:')
    incorrect = np.where(predicted_classes != raw_labels)[0]
    for i, incorrect in enumerate(np.random.choice(incorrect, 9)):
        plt.subplot(3, 3, i + 1)
        plt.imshow(IMAGES[incorrect].reshape(16, 16), cmap = 'gray', interpolation = 'none')
        plt.title("P: {}, L: {}".format(target_names[predicted_classes[incorrect]], target_names[raw_labels[incorrect]]))
        plt.tight_layout()

    plt.show()

    print(classification_report(LABELS, prep_labels(predicted_classes), target_names = target_names))

def main():
    history = train(MODEL, IMAGES, LABELS, OUTPUT)
    report(history, MODEL)

if __name__ == '__main__':
    main()

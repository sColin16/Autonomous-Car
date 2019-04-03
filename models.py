'''Defines all the different models that were tested as candidates for
the final self-driving model. Also reports validation accuracies achieved.'''

import keras
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU

# Consistently at about 0.80 validation accuracy
def modelA():
    print('Now Loading Model A. Created 3/22')

    model = Sequential()
    model.add(Conv2D(8, kernel_size=(3, 3), activation='linear',padding='same', input_shape = (16, 16, 1)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Conv2D(16, kernel_size=(3, 3), activation='linear',padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(16, activation='linear'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(0.25))
    model.add(Dense(3, activation='softmax'))

    model.summary()

    return model

# A wider version of model A
# Similar performance to model A: validation accuracy of about 0.8
def modelB():
    print('Now Loading Model B. Created 3/22')

    model = Sequential()
    model.add(Conv2D(16, kernel_size=(3, 3), activation='linear',padding='same', input_shape=(16, 16, 1)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Conv2D(32, kernel_size=(3, 3), activation='linear',padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(64, activation='linear'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(0.25))
    model.add(Dense(3, activation='softmax'))

    model.summary()

    return model

# Identical to model A, but uses the 32x32 images
# Also obtained a validation accuracy of 0.8
def modelC():
    print('Now Loading Model C. Created 3/22')

    model = Sequential()
    model.add(Conv2D(8, kernel_size=(3, 3), activation='linear',padding='same', input_shape=(32, 32, 1)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Conv2D(16, kernel_size=(3, 3), activation='linear',padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(32, activation='linear'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(0.25))
    model.add(Dense(3, activation='softmax'))

    model.summary()

    return model

# Identical to modelA, but without dropout. Also obtained 0.8 validation accuracy
def modelD():
    print('Now Loading Model D. Created 3/25')

    model = Sequential()
    model.add(Conv2D(8, kernel_size=(3, 3), activation='linear',padding='same', input_shape = (16, 16, 1)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Conv2D(16, kernel_size=(3, 3), activation='linear',padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Flatten())
    model.add(Dense(16, activation='linear'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dense(3, activation='softmax'))

    model.summary()

    return model

# Identical to modelA, but with another convolutional layer
# Does not improve upon the validation accuracy (still 0.8)
def modelE():
    print('Now Loading Model E. Created 3/25')

    model = Sequential()
    model.add(Conv2D(8, kernel_size=(3, 3), activation='linear',padding='same', input_shape = (16, 16, 1)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Conv2D(16, kernel_size=(3, 3), activation='linear',padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Conv2D(32, kernel_size=(3, 3), activation='linear',padding='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(16, activation='linear'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(0.25))
    model.add(Dense(3, activation='softmax'))

    model.summary()

    return model


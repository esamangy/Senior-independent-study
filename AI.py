import os
from random import randrange
from format_image import load_image, show_image

import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
train_images = []
test_images = []
path = ""


def init_data(size):
    test = []
    train = []
    global path
    path = "formatted_images" + str(size) + "x" + str(size) + "\\"
    files = os.listdir(path)
    for file in files:
        if randrange(7) == 0:
            if file[0] == 'R':
                real = 1
            else:
                real = 0
            test.append((file, real))
        else:
            if file[0] == 'R':
                real = 1
            else:
                real = 0
            train.append((file, real))
    load_data(test, 1)
    load_data(train, 0)


def load_data(files, test):
    global test_images, train_images
    for file in files:
        if test:
            test_images.append(load_image_for_ai(file))
        else:
            train_images.append(load_image_for_ai(file))


def load_image_for_ai(info):
    image = load_image(os.path.join(path, info[0]))
    return image, info[1]



import os
from random import randrange

import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
train_images = []
test_images = []


def load_data():
    files = os.listdir("formatted_images\\")
    for file in files:
        print(file)
        if randrange(7) == 0:
            if file[0] == 'R':
                real = 1
            else:
                real = 0
            test_images.append((file, real))
        else:
            if file[0] == 'R':
                real = 1
            else:
                real = 0
            train_images.append((file, real))

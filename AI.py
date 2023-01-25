import os
from random import randrange
from format_image import load_image, show_image, IMG_SIZE

import numpy as np
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
train_images = []
train_labels = [0, 1]
test_labels = ["fake", "real"]
test_images = []

path = ""
model = None


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
    preprocess_images()


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


# this method is used to make each pixel into a single data point to make the network smaller
def preprocess_images():
    global train_images, test_images
    temprow = np.empty(len(train_images[0][0][0]), dtype=int)
    tempimage = np.empty(len(train_images[0][0]), dtype=object)
    i = 0
    # for train_images
    for image, data in train_images:
        r = 0
        for row in image:
            p = 0
            for pix in row:
                temp = pix[0]
                temp = temp << 8
                temp = temp + pix[1]
                temp = temp << 8
                temp = temp + pix[2]
                temp = temp / 0xffffff
                temprow[r] = temp
                # error here
                p += 1
            tempimage[i] = temprow
            r += 1
        train_images[i] = tempimage
        i += 1

    # for test images
    for image, data in test_images:
        r = 0
        for row in image:
            p = 0
            for pix in row:
                temp = pix[0]
                temp = temp << 8
                temp = temp + pix[1]
                temp = temp << 8
                temp = temp + pix[2]
                temp = temp / 0xffffff
                temprow[r] = temp
                # error here
                p += 1
            tempimage[i] = temprow
            r += 1
        test_images[i] = tempimage
        i += 1


# this method will build the network itself
def build_network():
    global model
    if IMG_SIZE <= 256:
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE)),  # input layer (1)
            keras.layers.Conv1D(IMG_SIZE * 2, activation='relu'),  # hidden layer (2)
            keras.layers.Dense(IMG_SIZE / 2, activation='sigmoid'), # output layer (3)
            keras.layers.Dense(1, activation='softmax')  # output layer (4)
        ])
    elif IMG_SIZE <= 512:
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE)),  # input layer (1)
            keras.layers.Conv1D(IMG_SIZE * 4, activation='relu'),  # hidden layer (2)
            keras.layers.Dense(IMG_SIZE, activation='sigmoid'),  # output layer (3)
            keras.layers.Dense(1, activation='softmax')  # output layer (4)
        ])
    else:
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE)),  # input layer (1)
            keras.layers.Conv1D(IMG_SIZE * 6, activation='relu'),  # hidden layer (2)
            keras.layers.Dense(IMG_SIZE * 2, activation='sigmoid'),  # output layer (3)
            keras.layers.Dense(IMG_SIZE / 2, activation='sigmoid'),  # output layer (4)
            keras.layers.Dense(1, activation='softmax')  # output layer (5)
        ])


def compile_network():
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


def train(epochs):
    model.fit(train_images, train_labels, epochs)  # we pass the data, labels and epochs and watch the magic!


def evaluate():
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=1)
    print('Test accuracy:', test_acc)


def predict():
    predictions = model.predict(test_images)
    for pred in predictions:
        test_labels[np.argmax(pred)]


def load_test():
    pass


def load_ai(loadpath):
    global model
    model = keras.models.load_model(loadpath)


def save_ai(savepath):
    global model
    model.save(savepath)

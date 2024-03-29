# this file is responsible for all AI related functions and their helper functions
# this file is used by controller.py
import os
from sys import exit
from random import randrange
from format_image import load_image, show_image
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
train_images = []
train_labels = []
class_names = ["fake", "real"]
test_images = []
test_labels = []
IMG_SIZE = -1

path = ""
model = None
modelname = ""
loaded_size = -1


# helper function to get the name of the currently loaded model. Used to know if loading a new model is necessary
def get_model_name():
    return modelname


# helper function to set the IMG_SIZE variable of the AI.py file is set
def set_size(size):
    global IMG_SIZE
    IMG_SIZE = size


# this function will load a folder of images of IMG_SIZE and facilitate preprocessing them
def init_data(size):
    global loaded_size
    if loaded_size == size:
        return
    test = []
    train = []
    global path
    path = "formatted_images" + str(size) + "x" + str(size) + "\\"
    files = os.listdir(path)
    for file in files:
        if randrange(5) == 0:
            if file[0] == 'R':
                real = 1
            else:
                real = 0
            test.append(file)
            test_labels.append(real)
        else:
            if file[0] == 'R':
                real = 1
            else:
                real = 0
            train.append(file)
            train_labels.append(real)
    load_data(test, 1)
    load_data(train, 0)
    preprocess_images()
    loaded_size = size


# this is a helper function to add each loaded image to a local array
def load_data(files, test):
    global test_images, train_images
    for file in files:
        if test:
            test_images.append(load_image_for_ai(file))
        else:
            train_images.append(load_image_for_ai(file))


# this will return an image given a viable path to an image
def load_image_for_ai(info):
    image = load_image(os.path.join(path, info))
    return image


# this method is used to make each pixel into a single data point to make the network smaller
def preprocess_images():
    global train_images, test_images, IMG_SIZE
    IMG_SIZE = len(train_images[0][0])
    #= np.empty(len(train_images[0]) * len(train_images[0]), dtype=object)

    # for train_images
    i = 0
    for image in train_images:
        p = 0
        tempimage = []
        for row in image:
            temprow = []
            for pix in row:
                temp = pix[0]
                temp = temp << 8
                temp = temp + pix[1]
                temp = temp << 8
                temp = temp + pix[2]
                temp = temp / 0xffffff
                temprow.append(temp)
                p += 1
            tempimage.append(temprow)
        train_images[i] = tempimage
        i += 1

    # for test images
    i = 0
    for image in test_images:
        p = 0
        tempimage = []
        for row in image:
            temprow = []
            for pix in row:
                temp = pix[0]
                temp = temp << 8
                temp = temp + pix[1]
                temp = temp << 8
                temp = temp + pix[2]
                temp = temp / 0xffffff
                temprow.append(temp)
                p += 1
            tempimage.append(temprow)
        test_images[i] = tempimage
        i += 1


# this helper function will get the size of images from the folder name
def get_size():
    temp = modelname.split("x")
    size = 0
    for ch in temp[1]:
        if ch == "_":
            break
        else:
            size += int(ch)
            size *= 10
    size /= 10
    return int(size)


# this method will build the network itself into the currently loaded model
def build_network():
    global model
    if IMG_SIZE < 0:
        print("Invalid image size setup")
        exit(2)
    if IMG_SIZE <= 256:
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE)),  # input layer (1)
            keras.layers.Dense(IMG_SIZE * 2, activation='relu'),  # hidden layer (2)
            keras.layers.Dense(IMG_SIZE / 2, activation='sigmoid'),  # output layer (3)
            keras.layers.Dense(1, activation='sigmoid')  # output layer (4)
        ])
    elif IMG_SIZE <= 512:
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE)),  # input layer (1)
            keras.layers.Dense(IMG_SIZE * 4, activation='relu'),  # hidden layer (2)
            keras.layers.Dense(IMG_SIZE, activation='sigmoid'),  # output layer (3)
            keras.layers.Dense(1, activation='sigmoid')  # output layer (4)
        ])
    else:
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE)),  # input layer (1)
            keras.layers.Dense(IMG_SIZE * 6, activation='relu'),  # hidden layer (2)
            keras.layers.Dense(IMG_SIZE * 2, activation='sigmoid'),  # output layer (3)
            keras.layers.Dense(IMG_SIZE / 2, activation='sigmoid'),  # output layer (4)
            keras.layers.Dense(1, activation='sigmoid')  # output layer (5)
        ])


# this will compile the currently loaded network
def compile_network():
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # loss='sparse_categorical_crossentropy'


# this will train the currently loaded model
def train(e):
    global train_images, train_labels
    # print(len(train_images))
    # print(len(test_images))
    model.fit(train_images, train_labels, epochs=e)  # we pass the data, labels and epochs and watch the magic!


# this will evaluate the currently loaded model
def evaluate():
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=1)
    print('Test accuracy:', test_acc)


# this will print individual predictions until they run out or a c is input
def predict():
    predictions = model.predict(test_images)
    for predcntr in range(len(predictions)):
        predmsg = "Please press enter to view the next prediction, or type \"c\" to stop\n"
        inp = input(predmsg)
        if inp == "c":
            return
        print("The model Predicted: " + str(predictions[predcntr][0]))
        print("The correct answer is: " + str(test_labels[predcntr]))


# this will load a model
def load_ai(loadpath):
    global model, modelname
    try:
        model = keras.models.load_model(loadpath)
        modelname = loadpath
        return 0
    except FileNotFoundError:
        print("The path was not valid")
        return 1
    except IOError:
        print("The path was not valid")
        return 2


# this will save a model to the savepath name
def save_ai(savepath):
    global model, modelname
    modelname = savepath
    model.save(savepath)

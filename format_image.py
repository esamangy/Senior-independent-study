# this file is responsible for loading, formatting, and saving images.
# this file is used by controller.py
from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte
import os
import re

import matplotlib.pyplot as plt
IMG_SIZE = -1


# sets the format_image.py file IMG_SIZE to size
def format_init(size):
    global IMG_SIZE
    IMG_SIZE = size


# Given a path, this function will load every image in the folder and format them to the IMG_SIZE
# if it can't open a folder with images it will return an error
def format_directory(path):
    if re.search("formatted_images" + str(IMG_SIZE) + "x" + str(IMG_SIZE), path):
        print("already formatted")
        return
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        raise FileNotFoundError
    except NotADirectoryError:
        raise NotADirectoryError
    numimages = 0
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            numimages += 1
    if numimages < 1:
        raise ValueError
    i = 0
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            print("Processing images " + str(i) + " of " + str(numimages))
            format_image(os.path.join(path, file), file)
            i += 1
    print("Processing images " + str(i) + " of " + str(numimages))


# This function will format a single image given a path to a folder, and the name of the image.
# It will crop, resize and save in that order (very important order)
def format_image(path, name):
    uncropped = load_image(path)
    if uncropped.shape is not (IMG_SIZE, IMG_SIZE, 3):
        cropped = crop_image(uncropped)
        resized = resize_image(cropped)
    save_image(resized, name)
    # return resized


# this will return an image given a path to an image
def load_image(path):
    return io.imread(path)


# will crop the given image to square by finding th smaller of the sides
def crop_image(image):
    size = image.shape
    height = size[1]
    width = size[0]
    if width > height:
        diff = int((width - height) / 2)
        cropped = image[diff: width - diff, 0: height]
    else:
        diff = int((height - width) / 2)
        cropped = image[0: width, diff: height - diff]
    return cropped


# this will resize an image to IMG_SIZE
def resize_image(image):
    return resize(image, (IMG_SIZE, IMG_SIZE))


# This will save the image to a folder named formatted_images<IMG_ISIZE>_<IMG_SIZE>
# if that folder doesn't exist it will create that folder
def save_image(image, name):
    path = "formatted_images" + str(IMG_SIZE) + "x" + str(IMG_SIZE) + "\\" + name
    tosave = img_as_ubyte(image)
    try:
        io.imsave(path, tosave)
    except FileNotFoundError:
        os.mkdir("formatted_images" + str(IMG_SIZE) + "x" + str(IMG_SIZE) + "\\")
        io.imsave(path, tosave)


# this is a utility function used in debuging. It will display the image.
def show_image(image):
    io.show()
    io.imshow(image)
    plt.show()

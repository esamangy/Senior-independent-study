from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte
import os
import re

import matplotlib.pyplot as plt
IMG_SIZE = -1


def format_init(size):
    global IMG_SIZE
    IMG_SIZE = size


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


def format_image(path, name):
    uncropped = load_image(path)
    if uncropped.shape is not (IMG_SIZE, IMG_SIZE, 3):
        cropped = crop_image(uncropped)
        resized = resize_image(cropped)
    save_image(resized, name)
    # return resized


def load_image(path):
    return io.imread(path)


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


def resize_image(image):
    return resize(image, (IMG_SIZE, IMG_SIZE))


def save_image(image, name):
    #cntr = get_image_cntr() + 1
    path = "formatted_images" + str(IMG_SIZE) + "x" + str(IMG_SIZE) + "\\" + name
    tosave = img_as_ubyte(image)
    try:
        io.imsave(path, tosave)
    except FileNotFoundError:
        os.mkdir("formatted_images" + str(IMG_SIZE) + "x" + str(IMG_SIZE) + "\\")
        io.imsave(path, tosave)


def show_image(image):
    io.show()
    io.imshow(image)
    plt.show()

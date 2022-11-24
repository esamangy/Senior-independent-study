from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte
import os

import matplotlib.pyplot as plt
IMG_SIZE = -1
SAVE_IMAGE = -1


def format_init():
    global IMG_SIZE, SAVE_IMAGE
    with open("settings", 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.find('size') != -1:
                temp = ''
                for char in line:
                    if char.isdigit():
                        temp += char
                IMG_SIZE = int(temp)
            if line.find('save') != -1:
                temp = ''
                for char in line:
                    if char.isdigit():
                        temp += char
                if int(temp):
                    SAVE_IMAGE = 1
                else:
                    SAVE_IMAGE = 0


def format_directory(path):
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
            format_image(os.path.join(path, file))
            i += 1
    print("Processing images " + str(i) + " of " + str(numimages))


def format_image(path):
    uncropped = load_image(path)
    cropped = crop_image(uncropped)
    resized = resize_image(cropped)
    if SAVE_IMAGE:
        save_image(resized)
    return resized


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
    return resize(image, (IMG_SIZE, IMG_SIZE, 3))


def save_image(image):
    cntr = get_image_cntr() + 1
    path = "formatted_images/" + str(cntr) + ".jpg"
    tosave = img_as_ubyte(image)
    try:
        io.imsave(path, tosave)
    except FileNotFoundError:
        os.mkdir("formatted_images/")
        io.imsave(path, tosave)


def get_image_cntr():
    with open("settings", 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        cntr = ''
        for line in lines:
            if line.find('cntr') != -1:
                for char in line:
                    if char.isdigit():
                        cntr += char
        file.seek(0)
        text = file.read()
        file.seek(text.find('cntr') + 6)
        num = int(cntr) + 1
        file.write(str(num) + "\n")
        return int(cntr)




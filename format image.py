from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte

import matplotlib.pyplot as plt
IMG_SIZE = 128


def format_image(path):
    uncropped = load_image("unknown_images/test.jpg")
    cropped = crop_image(uncropped)
    resized = resize_image(cropped)
    return resized


def format_and_save(path):
    uncropped = load_image(path)
    cropped = crop_image(uncropped)
    resized = resize_image(cropped)
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
    path = "formated_images/" + str(cntr) + ".jpg"
    tosave = img_as_ubyte(image)
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
        file.seek(text.find('cntr') + 5)
        num = int(cntr) + 1
        file.write(str(num) + "\n")
        return int(cntr)


if __name__ == "__main__":
    format_and_save("unknown_images/test1.jpg", )

from skimage import io
from skimage.transform import resize

import matplotlib.pyplot as plt
IMG_SIZE = 128



def save_formated_image(path,):
    uncropped = load_image(path)
    cropped = crop_image(uncropped)
    resized = resize_image(cropped)
    save_image(resized, save_cntr)


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


def save_image(image, cntr):
    path = "formated_images/" + str(cntr) + ".jpg"
    io.imsave(path, image)

    #io.imshow(uncropped_gray)
    #io.show()
    #save new image in different folder




if __name__ == "__main__":
    main()

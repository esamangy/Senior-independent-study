# this file will be used as a controller to control all aspects of the program
import os
from format_image import format_image, format_init


training = None
size = -1
save = None


def main():
    # get input
    get_user_settings()
    update_settings()
    # init everything
    format_init()


    #format_image('unknown_images/test4.jpg')


def get_user_settings():
    global training, size, save
    message = "For training enter 1. For testing enter 2:"
    while 1:
        inp = input(message)
        if int(inp) == 1:
            training = True
            break
        elif int(inp) == 2:
            training = False
            break
        else:
            message = "please enter a 1 or 2"
    message = "Please enter a valid image size. The images will be square so only one number is needed.\n" \
              "I recommend a size between 256 and 512 however any size will do.\n" \
              "The size must be at least 128. Larger images will take longer to process"
    while 1:
        inp = input(message)
        if not inp.isdigit():
            message = "Your size must be a valid integer"
        elif int(inp) >= 128:
            size = int(inp)
            break
        else:
            message = "Your size must be at least 128"
    message = "Would you like to save any images that need formatting. Formatting means cropping the images to\n" \
              "square to the size you just input of " + str(size) + ". This will not overwrite your images but it\n" \
              "will overwrite any previously formatted images. This will make current runtime longer but increase\n" \
              "speed for any future runs on the same set. Type \"yes\" to save or \"no\" to skip this."
    while 1:
        inp = input(message)
        if inp.lower() == "yes":
            save = 1
            break
        elif inp.lower() == "no":
            save = 0
            break
        else:
            message = "Please type yes or no"


def update_settings():
    with open("settings", 'w', encoding='utf-8') as file:
        file.write('size' + size + '\n')
        file.write('save' + save + '\n')
        if save == 1:
            file.write('cntr' + '0')


if __name__ == "__main__":
    main()

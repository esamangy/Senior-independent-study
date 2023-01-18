# this file will be used as a controller to control all aspects of the program
import os
from format_image import format_directory, format_init
from AI import init_data, build_network, compile_network, train, evaluate


training = None
size = -1
save = None


def main():
    # get input
    get_user_settings()
    update_settings()
    # init everything
    format_init()
    get_and_use_directory_path()
    init_data(size)
    build_network()
    compile_network()
    train()
    evaluate()


def get_and_use_directory_path():
    message = "Please enter a valid path to a folder with images to be used."
    while 1:
        inp = input(message)
        try:
            format_directory(inp)
            break
        except FileNotFoundError:
            message = "The folder you input does not exist, please input another path"
        except NotADirectoryError:
            message = "The path you input was not to a directory, please input another path"
        except ValueError:
            message = "The directory you input has no images, please input another path"
    return


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
    # message = "Would you like to save any images that need formatting. Formatting means cropping the images to\n" \
    #           "square to the size you just input of " + str(size) + ". This will not overwrite your original images " \
    #           "but it\nwill overwrite any previously formatted images. This will make initial runtime longer but " \
    #           "increase\nspeed for later processing. Type \"yes\" to save or \"no\" to skip this."
    # while 1:
    #     inp = input(message)
    #     if inp.lower() == "yes":
    #         save = 1
    #         break
    #     elif inp.lower() == "no":
    #         save = 0
    #         break
    #     else:
    #         message = "Please type yes or no"


def update_settings():
    with open("settings.txt", 'w', encoding='utf-8') as file:
        file.write('size' + str(size) + '\n')
        # file.write('save' + str(save) + '\n')
        file.write('save' + '1' + '\n')
        #if save == 1:
            #file.write('cntr' + '0')


if __name__ == "__main__":
    main()

# this file will be used as a controller to control all aspects of the program
import os
from format_image import format_image, format_init


def main():
    format_init()
    format_image('unknown_images/test4.jpg')


if __name__ == "__main__":
    main()

# this file will be used as a controller to control all aspects of the program
from format_image import format_directory, format_init
from AI import *

training = None
size = -1
epochs = -1
baseask = "Please enter a 1 for image editing\nPlease enter a 2 for network building\n" \
          "Please enter a 3 for model training\nPlease enter a 4 for model testing\nPlease enter a 5 to quit\n"


def main():
    inp = int(input(baseask))
    while inp != 5:
        if inp == 1:
            image_edit_control()
        elif inp == 2:
            network_build_control()
        elif inp == 3:
            train_control()
        elif inp == 4:
            test_control()
        else:
            print("Please enter a number from 1-5")
        inp = int(input(baseask))
    print("Thank You")


def image_edit_control():
    global size
    editmsg = "You are now in the Image editing section, to begin editing images for the AI\n" \
              "please enter the path to a folder with the unedited images in it or type 1 to go back\n"
    inp = input(editmsg)
    if inp.isdigit() and int(inp) == 1:
        return
    pathcheck = False
    while (inp.isdigit() and int(inp) == 1) or pathcheck:
        pathcheck = check_directory_path(inp)
    p = inp
    editmsg = "Please enter a valid image size. The images will be square so only one number is needed.\n" \
              "It is recommended to use a size between 256 and 512 however any size will do.\n" \
              "The size must be at least 128. Larger images will take longer to process\n"
    while 1:
        inp = input(editmsg)
        if not inp.isdigit():
            editmsg = "Your size must be a valid integer"
        elif int(inp) >= 128:
            size = int(inp)
            break
        else:
            editmsg = "Your size must be at least 128"
    print("Please wait while your images are being formatted")
    format_init(size)
    format_directory(p)


def network_build_control():
    buildmsg = "You are now in the network building section, to begin building the network of the AI\n" \
               "please enter the path to a folder with the EDITED images in it or type 1 to go back\n"
    isize = -1
    while isize < 0:
        inp = input(buildmsg)
        if inp.isdigit() and int(inp) == 1:
            return
        pathcheck = False
        while (inp.isdigit() and int(inp) == 1) or pathcheck:
            pathcheck = check_directory_path(inp)
        p = inp
        try:
            files = os.listdir(p)
        except FileNotFoundError:
            raise FileNotFoundError
        except NotADirectoryError:
            raise NotADirectoryError
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                tempimage = load_image(os.path.join(p, file))
                isize = tempimage.shape[0]
                break
        if not isize < 0:
            buildmsg = "The path you entered did not have images with a proper size. Please enter a new path\n"

    buildmsg = "The size of the images in this folder are: " + str(isize) + "\nWould you like to " \
                                                                            "use this folder as a template?\n" \
               "Please type a \"y\" to continue building or a \"n\" to cancel\n"
    while 1:
        inp = input(buildmsg)
        if inp.lower() == "y":
            print("Building model for size " + str(isize) + " images")
            break
        elif inp.lower() == "n":
            print("Cancelling build. Returning to main menu\n")
            return
        else:
            buildmsg = "Please enter a \"y\" to continue building or a \"n\" to cancel\n"
    set_size(isize)
    build_network()
    compile_network()
    temp = "Model" + str(isize) + "x" + str(isize) + "_" + str(0)
    save_ai(temp)
    print("The model has been saved as: " + temp)


def train_control():
    trainmsg = "You are now in the training section, The current loaded model is: " + get_model_name() + \
               "\nPlease enter a \"y\" to continue working with this model, or a \"n\" to change models.\n" \
               "Or enter a 1 to go back to the main menu\n"
    needmodel = True
    while needmodel:
        inp = input(trainmsg)
        if inp.isdigit() and int(inp) == 1:
            return
        if inp.lower() == "y":
            print("Continuing training with: " + get_model_name())
            needmodel = False
        elif inp.lower() == "n":
            trainmsg = "Please enter the path to a folder with the model in it or type 1 to go back\n" \
                       "The model should have a name similar to \"Model<SIZE>x<SIZE>_<INT>\"\n"
            pathcheck = False
            while not pathcheck:
                inp = input(trainmsg)
                if load_ai(inp) == 0:
                    pathcheck = True
                    needmodel = False
                else:
                    trainmsg = "Please enter a a valid path"
        else:
            trainmsg = "Please enter a \"y\" to continue with the current model or a \"n\" to change models\n"
        p = get_model_name()
        trainmsg = "Please enter a valid number of epochs you would like to train for\n"
        while 1:
            inp = input(trainmsg)
            if not inp.isdigit():
                trainmsg = "Your size must be a valid integer\n"
            elif int(inp) <= 0:
                trainmsg = "The number of epochs must be at least 1\n"
            else:
                print("Now training for " + inp + " epochs. Please wait.\n")
                temp = p.split("x")
                size = 0
                for ch in temp[1]:
                    if ch == "_":
                        break
                    else:
                        size += int(ch)
                        size *= 10
                size /= 10
                init_data(int(size))
                train(int(inp))
                break
        temp = p.split("_")
        num = ""
        for ch in temp[1]:
            if ch.isdigit():
                num += ch
        newname = temp[0] + "_" + str(int(num) + int(inp))
        save_ai(newname)
        print("The model has been saved as: " + newname)


def test_control():
    pass


def old():
    # get input
    get_user_settings()
    update_settings()
    # init everything
    if training:
        format_init()
        #get_and_use_directory_path()
        init_data(size)
        print("Building and compiling network")
        build_network()
        compile_network()
        print("Training network now")
        train(epochs)
        print("Evaluating network")
        evaluate()
        if save:
            temp = "Model" + str(size) + "x" + str(size) + "_" + str(epochs)
            save_ai(temp)
            print("The model has been saved as: " + temp)
    else:
        load_ai()
        load_test()


def check_directory_path(p):
    try:
        os.access(p, os.F_OK)
    except FileNotFoundError:
        print("The folder you input does not exist, please input another path")
        return False
    except NotADirectoryError:
        print("The path you input was not to a directory, please input another path")
        return False
    except ValueError:
        print("The directory you input has no images, please input another path")
        return False
    return True


def get_user_settings():
    global training, size, save, epochs
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
    message = "How many epochs would you like to train for. More epochs will take longer " \
              "and not necessarily lead to higher accuracy. Keep overtraining in mind too."
    while 1:
        inp = input(message)
        if not inp.isdigit():
            message = "Your size must be a valid integer"
        elif int(inp) > 0:
            epochs = int(inp)
            break
        else:
            message = "Your size must be at least 0"
    message = "Would you like to save the model. Y for yes, N for no"
    while 1:
        inp = input(message)
        if not inp.isalpha():
            message = "You must enter a letter"
        elif inp.lower() == 'y':
            save = True
            break
        elif inp.lower() == 'n':
            save = False
            break
        else:
            print(inp.lower() == 'y')
            message = "You must enter a \'Y\' or a \'N\'"


def update_settings():
    with open("settings.txt", 'w', encoding='utf-8') as file:
        file.write('size' + str(size) + '\n')
        # file.write('save' + str(save) + '\n')
        file.write('save' + '1' + '\n')
        #if save == 1:
            #file.write('cntr' + '0')


if __name__ == "__main__":
    main()

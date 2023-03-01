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
            init_data(get_size())
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
    testmsg = "You are now in the testing section, The currently loaded model is: " + get_model_name() + \
               "\nPlease enter a \"y\" to continue working with this model, or a \"n\" to change models.\n" \
               "Or enter a 1 to go back to the main menu\n"
    needmodel = True
    while needmodel:
        inp = input(testmsg)
        if inp.isdigit() and int(inp) == 1:
            return
        if inp.lower() == "y":
            print("Continuing testing with: " + get_model_name())
            needmodel = False
        elif inp.lower() == "n":
            testmsg = "Please enter the path to a folder with the model in it or type 1 to go back\n" \
                       "The model should have a name similar to \"Model<SIZE>x<SIZE>_<INT>\"\n"
            pathcheck = False
            while not pathcheck:
                inp = input(testmsg)
                if load_ai(inp) == 0:
                    pathcheck = True
                    needmodel = False
                else:
                    testmsg = "Please enter a a valid path"
        else:
            testmsg = "Please enter a \"y\" to continue with the current model or a \"n\" to change models\n"
    testmsg = "Would you like to evaluate the Model or see its predictions?\n" \
              "Please enter an \"e\" to evaluate, a \"p\" to predict, or enter a \"c\" to cancel\n"
    while 1:
        inp = input(testmsg)
        if not inp.isalpha():
            testmsg = "You must enter an \"e\" to evaluate, a \"p\" to predict, or enter a \"c\" to cancel\n"
        elif inp == "e":
            print("Evaluating the Model\n")
            init_data(get_size())
            evaluate()
            testmsg = "Please enter an \"e\" to evaluate, a \"p\" to predict, or enter a \"c\" to cancel\n"
        elif inp == "p":
            print("Now getting the Model's predictions")
            init_data(get_size())
            predict()
            testmsg = "Please enter an \"e\" to evaluate, a \"p\" to predict, or enter a \"c\" to cancel\n"
        elif inp == "c":
            return
        else:
            testmsg = "You must enter an \"e\" to evaluate, a \"p\" to predict, or enter a \"c\" to cancel\n"


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


if __name__ == "__main__":
    main()

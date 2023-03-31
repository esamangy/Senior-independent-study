# Senior-independent-study

# There are three main parts of the code which have been separated into separate files.

1) AI.py
This file is responsible for all AI related functions and is where the code which
manages the currently loaded ai is located.

2)format_image.py
This file hold all the relevant code for the image editing portion of the code.
There are functions to load, edit, and save images. It even has unused debugging
code to show the images.

3) controller.py
This file is the main file and is where the code opens from. This file holds the
code for each of the main subroutines within the code. It is the main state manager
and handles most errors which the user may encounter

# dependencies
tensorflow 2.10.1 and its dependencies (main Ai module)
scikit-image 0.19.3 (main image editing module)
matplotlib 3.6.1 (used for image handling and display)
os (directory and pathing)
re (regular expression searching)

## optional
time (used to measure training time. By commenting out the 2 lines this becomes unnecessary)

# The main file in the project

import numpy as np

DEFAULT_SNOW_DEPTH = 5

# Tree search
#   State:
#      - current location of shoveller
#      - current snow levels
#   Transition:
#      - move to an adjacent square
#      - snow moves from current square to destination square
#   Goal:
#      - All "driveway" tiles have snow levels of 0

def generate_driveway(width, height):
    x = np.ones((width + 2, height), float) * DEFAULT_SNOW_DEPTH
    return x


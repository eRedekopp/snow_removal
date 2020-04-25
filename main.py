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

# A state looks like this: { "driveway" : <array>, "xpos" : x, "ypos" : y }
# An action looks like this: ("walk", "down")

def initial_state(width, height, depth):
    """
    Get the initial problem state
    :param width: The width of the driveway
    :param height: The height of the driveway
    :param depth: The depth of snow on the driveway
    """
    driveway = np.ones((width + 2, height), float) * depth
    xpos = 1
    ypos = 0
    return {"driveway" : driveway,
            # Todo this is shit
            "driveway_tiles" : [(0, 1), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2)],
            "elapsed_time" : 0,
            "xpos" : xpos, 
            "ypos" : ypos}


def actions(state):
    """
    Return a list of all actions that can be taken from the given state
    :param state: A state
    :return: a list of all actions that we can take from the given state
    """
    pos_acts = []  # possible actions

    can_shovel = state["driveway"][state["xpos"]][state["ypos"]] > 0

    if can_shovel:
        pos_acts.append("shovel_left")
        pos_acts.append("shovel_right")

    if (state["xpos"] - 1, state["ypos"]) in state["driveway_tiles"]:
        pos_acts.append("walk_left")

    if (state["xpos"] + 1, state["ypos"]) in state["driveway_tiles"]:
        pos_acts.append("walk_right")

    if (state["xpos"], state["ypos"] - 1) in state["driveway_tiles"]:
        pos_acts.append("walk_up")
        if can_shovel:
            pos_acts.append("shovel_up")

    if (state["xpos"], state["ypos"] + 1) in state["driveway_tiles"]:
        pos_acts.append("walk_down")
        if can_shovel:
            pos_acts.append("shovel_down")

    if (state["xpos"] - 1, state["ypos"] - 1) in state["driveway_tiles"]:
        pos_acts.append("walk_upleft")
    if state["ypos"] != 0 and can_shovel:
        pos_acts.append("shovel_upleft")
        pos_acts.append("shovel_upright")

    if (state["xpos"] - 1, state["ypos"] + 1) in state["driveway_tiles"]:
        pos_acts.append("walk_downleft")
    if state["ypos"] != len(state["driveway"]) and can_shovel:
        pos_acts.append("shovel_downleft")
        pos_acts.append("shovel_downright")

    if (state["xpos"] + 1, state["ypos"] - 1) in state["driveway_tiles"]:
        pos_acts.append("walk_upright")

    if (state["xpos"] + 1, state["ypos"] + 1) in state["driveway_tiles"]:
        pos_acts.append("walk_downright")

    return pos_acts


def result(action, state):
    """
    Given an action and the state from which that action was taken, return the new state
    resulting from taking that action
    :param action: An action, as returned from actions()
    :param state: The state from which we took the action
    :return: The state resulting from taking the action
    """
    act, direction = action.split('_')

    if direction == "left":
        targetx = state["xpos"] - 1
        targety = state["ypos"]
    elif direction == "right":
        targetx = state["xpos"] + 1
        targety = state["ypos"]
    elif direction == "up":
        targetx = state["xpos"]
        targety = state["ypos"] - 1
    elif direction == "down":
        targetx = state["xpos"]
        targety = state["ypos"] + 1
    elif direction == "downleft":
        targetx = state["xpos"] - 1
        targety = state["ypos"] + 1
    elif direction == "downright":
        targetx = state["xpos"] + 1
        targety = state["ypos"] + 1
    elif direction == "upleft":
        targetx = state["xpos"] - 1
        targety = state["ypos"] - 1
    elif direction == "upright":
        targetx = state["xpos"] + 1
        targety = state["ypos"] - 1
    else:
        raise RuntimeError

    new_state = state.copy()

    if act == "walk":
        new_state["xpos"] = targetx
        new_state["ypos"] = targety
        new_state["elapsed_time"] += 1

    elif act == "shovel":
        cur_snow = state["driveway"][state["xpos"]][state["ypos"]]
        new_state["driveway"][targetx][targety] += cur_snow
        state["driveway"][state["xpos"]][state["ypos"]] = 0
        if cur_snow < 10:
            new_state["elapsed_time"] = 1.5
        else:
            new_state["elapsed_time"] = 1.5 + (cur_snow - 10) * 0.1

    return new_state


def is_goal(state):
    """
    Is this state our goal state?
    """
    for x, y in state["driveway_tiles"]:
        if state["driveway"][x][y] != 0:
            return False
    return True

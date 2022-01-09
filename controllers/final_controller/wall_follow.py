import bug2_algorithm
from motion import *

wall_to_right = False
wall_to_left = False

"""assumes robot is already parallel to wall"""


def wall_follow():
    global wall_to_right
    global wall_to_left

    if not bug2_algorithm.wall_in_front:
        move_forward()

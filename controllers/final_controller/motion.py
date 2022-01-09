from random import choice

from initialization import *

speed = 7
rotate_speed = 4


def move_forward():
    update_motor_speed(input_omega=[-speed, speed, 0])


""" :param clockwise: -1 | anti-clockwise : 1 """


def inplace_rotate(current_heading_degree, destination_degree, direction=1):
    if abs(destination_degree - current_heading_degree) >= 1 or abs(destination_degree - current_heading_degree) >= 359:
        update_motor_speed(input_omega=[rotate_speed * direction, rotate_speed * direction, rotate_speed * direction])
        return False
    else:
        update_motor_speed(input_omega=[0, 0, 0])
        return True


def head_to_destination(theta, robot_position, goal_position):
    rotation_val = np.arctan2(goal_position[1] - robot_position[1], goal_position[0] - robot_position[0])

    # to degree & shift
    rotation_val = rotation_val / math.pi * 180.0

    return inplace_rotate(theta, rotation_val)

from random import choice

from initialization import *

speed = 7


def move_forward():
    update_motor_speed(input_omega=[-speed, speed, 0])


def inplace_rotate(current_heading_degree, destination_degree):
    # buggy when dest == 0
    if destination_degree - current_heading_degree > 1 or destination_degree - current_heading_degree < -1:
        update_motor_speed(input_omega=[3, 3, 3])
        return False
    else:
        update_motor_speed(input_omega=[0, 0, 0])
        return True


def head_to_destination(theta, robot_position, goal_position):
    rotation_val = np.arctan2(goal_position[1] - robot_position[1], goal_position[0] - robot_position[0])

    # to degree & shift
    rotation_val = rotation_val / math.pi * 180.0

    return inplace_rotate(theta, rotation_val)

#
# def inplace_random_turn_90():
#     dir = choice(['left', 'right'])
#     if dir == 'left':
#         inplace_rotate(theta, destination_degree)
#     else:
#         inplace_rotate(theta, destination_degree)

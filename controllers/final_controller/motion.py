from initialization import *

speed = 7


def move_forward():
    update_motor_speed(input_omega=[-speed, speed, 0])


def inplace_rotate(current_heading_degree, rotate_degree):
    if rotate_degree - current_heading_degree > 1 or rotate_degree - current_heading_degree < -1:
        update_motor_speed(input_omega=[3, 3, 3])
    else:
        update_motor_speed(input_omega=[0, 0, 0])


def head_to_destination(theta, robot_position, goal_position):
    rotation_val = np.arctan2(goal_position[1] - robot_position[1], goal_position[0] - robot_position[0])

    # to degree & shift
    rotation_val = rotation_val / math.pi * 180.0

    inplace_rotate(theta, rotation_val)
    print(theta, rotation_val)

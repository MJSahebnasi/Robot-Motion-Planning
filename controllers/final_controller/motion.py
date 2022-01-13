import bug2_algorithm
from initialization import *
import sense

speed = 7
rotate_speed = 4


def move_forward():
    update_motor_speed(input_omega=[-speed, speed, 0])


def move_forward_little_to_right():
    update_motor_speed(input_omega=[-speed, speed + 2, 0])


def move_forward_little_to_left():
    update_motor_speed(input_omega=[-speed - 2, speed, 0])


""" :param direction: clockwise: 1 | anti-clockwise : -1 """


def inplace_rotate(current_heading_degree, destination_degree, direction=1):
    if not sense.degrees_equal(current_heading_degree, destination_degree):
        update_motor_speed(input_omega=[rotate_speed * direction, rotate_speed * direction, rotate_speed * direction])
        return False
    else:
        update_motor_speed(input_omega=[0, 0, 0])
        return True


def head_to_destination(theta, robot_position, goal_position):
    rotation_val = np.arctan2(goal_position[1] - robot_position[1], goal_position[0] - robot_position[0])

    # to degree & shift
    rotation_val = (rotation_val / math.pi * 180.0) % 360

    # smart direction
    if (theta - rotation_val) % 360 < 180:
        dir = 1
    else:
        dir = -1

    return inplace_rotate(theta, rotation_val, dir)


def turn_corner_left(desired_heading):
    if sense.degrees_equal(bug2_algorithm.robot_heading, desired_heading):
        update_motor_speed(input_omega=[0, 0, 0])
        return True
    else:
        update_motor_speed(input_omega=[-7, 0, 0])
        return False


def turn_corner_right(desired_heading):
    if sense.degrees_equal(bug2_algorithm.robot_heading, desired_heading):
        update_motor_speed(input_omega=[0, 0, 0])
        return True
    else:
        update_motor_speed(input_omega=[0, 7, 0])
        return False

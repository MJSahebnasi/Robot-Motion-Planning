import bug1_algorithm
from initialization import *
import sense_bug1

speed = 10
rotate_speed = 3


def move_forward():
    update_motor_speed(input_omega=[-speed, speed, 0])


def move_forward_little_to_right():
    update_motor_speed(input_omega=[-speed, speed + 2, 0])


def move_forward_little_to_left():
    update_motor_speed(input_omega=[-speed - 2, speed, 0])


""" :param clockwise: 1 | anti-clockwise : -1 """


def inplace_rotate(current_heading_degree, destination_degree, direction=1):
    if not sense_bug1.degrees_equal(current_heading_degree, destination_degree):
        update_motor_speed(input_omega=[rotate_speed * direction, rotate_speed * direction, rotate_speed * direction])
        return False
    else:
        update_motor_speed(input_omega=[0, 0, 0])
        return True


def head_to_destination(theta, robot_position, goal_position):
    rotation_val = np.arctan2(goal_position[1] - robot_position[1], goal_position[0] - robot_position[0])

    # to degree & shift
    rotation_val = (rotation_val / math.pi * 180.0) % 360

    return inplace_rotate(theta, rotation_val)


def turn_corner_left(desired_heading):
    if sense_bug1.degrees_equal(bug1_algorithm.robot_heading, desired_heading):
        update_motor_speed(input_omega=[0, 0, 0])
        return True
    else:
        update_motor_speed(input_omega=[-7, 0, 0])
        return False


def turn_corner_right(desired_heading):
    if sense_bug1.degrees_equal(bug1_algorithm.robot_heading, desired_heading):
        update_motor_speed(input_omega=[0, 0, 0])
        return True
    else:
        update_motor_speed(input_omega=[0, 7, 0])
        return False

from initialization import *

speed = 7


def move_forward():
    update_motor_speed(input_omega=[-speed, speed, 0])


def inplace_rotate(current_heading_degree, rotate_degree):
    if rotate_degree - current_heading_degree > 1 or rotate_degree - current_heading_degree < -1:
        update_motor_speed(input_omega=[3, 3, 3])
    else:
        update_motor_speed(input_omega=[0, 0, 0])

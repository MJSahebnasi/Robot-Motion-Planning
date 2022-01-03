from initialization import *

speed = 6


def inplace_rotate():
    update_motor_speed(input_omega=[speed, speed, speed])


def move_forward():
    update_motor_speed(input_omega=[speed, -speed, 0])

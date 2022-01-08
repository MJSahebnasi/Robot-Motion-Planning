from initialization import *

speed = 7


def inplace_rotate():
    update_motor_speed(input_omega=[speed, speed, speed])


def move_forward():
    update_motor_speed(input_omega=[speed, -speed, 0])


def inplace_rotate(degree):
    gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()
    if degree - getBearingInDegrees(compass_val) > 1 or degree - getBearingInDegrees(compass_val) < -1:
        update_motor_speed(input_omega=[3, 3, 3])
    else:
        update_motor_speed(input_omega=[0, 0, 0])

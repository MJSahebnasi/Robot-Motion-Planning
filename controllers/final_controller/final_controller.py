# important points:
# use <robot_position> to get current position of robot in <x,y,theta> format.
# use <robot_omega> to get current values for the wheels in <w1,w2,w3> format.


import numpy as np

from bug2_algorithm import bug2
from initialization import *
from motion import *
from sense import *

goal_position = np.array([1.3, 6.15])  # <x,y>
initial_position = [1.3, -9.74]

if __name__ == "__main__":

    TIME_STEP = 32
    robot = init_robot(time_step=TIME_STEP)
    init_robot_state(in_pos=[0, 0, 0], in_omega=[0, 0, 0])

    while robot.step(TIME_STEP) != -1:
        # bug0()
        # bug1()
        bug2()
        # speed = 8
        # update_motor_speed(input_omega=[-12,5.5,-6])
    pass

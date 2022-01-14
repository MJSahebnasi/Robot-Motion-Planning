from cmath import inf
from random import choice
from enum import Enum
import time
from initialization import *
import motion_bug1
from sense_bug1 import *
import wall_follow_bug1
import final_controller


class Bug1_State(Enum):
    init = 1
    line_follow = 2
    get_parallel_to_wall = 3
    wall_follow_bug1 = 4
    reached_destination = 5
    cannot_reach_destination = 6


threshold = 0.08

# head: sonar[1], ir[0], ir[3]
# right front : ir[5]
# left front : ir[1]

robot_heading = None

wall_in_front = False

gps_values = None
compass_val = None
sonar_value = None
encoder_value = None
ir_value = None
least_distance = inf
rotate_final_degree = None
rotation_dir = None
# NEVER update stuff when robot is rotating
is_rotating = False

tic = 0
def update_least_distance():
    global least_distance
    global tic
    distance = ( (gps_values[0] - final_controller.goal_position[0])**2 + (gps_values[1] - final_controller.goal_position[1])**2 )**(0.5)
    if distance < least_distance:
        least_distance = distance
        tic = time.perf_counter()
        print("tic: ", tic)
    if abs(distance - least_distance) < 0.3:
        toc = time.perf_counter()
        if toc - tic > 240:
            print("it is turning")
            # We understand that we are in the second turn and on the least-distant point to the goal
            # motion_bug1.head_to_destination(robot_heading, gps_values, final_controller.goal_position)
            # bug1.state = Bug1_State.line_follow
            # motion_bug1.move_forward()
            if motion_bug1.head_to_destination(robot_heading, gps_values, final_controller.goal_position):
                bug1.prev_state = bug1.state
                bug1.state = Bug1_State.line_follow


    print("Done! : Least distance so far:", least_distance)



def setup():
    global rotation_dir
    global rotate_final_degree
    global is_rotating

    global wall_in_front

    global robot_heading
    robot_heading = get_bearing_in_degrees(compass_val)

    # NEVER update stuff when robot is rotating
    if not is_rotating and not wall_follow_bug1.is_rotating:
        # any wall around?
        wall_in_front = avoid_wall_in_front(sonar_value[1], ir_value[0], ir_value[3])
        # front-right IR
        if ir_value[5] < 1000:
            wall_follow_bug1.wall_to_right = True
        else:
            if wall_follow_bug1.wall_to_right:
                wall_follow_bug1.previously_wall_to_right = True
                wall_follow_bug1.previously_wall_to_left = False
            wall_follow_bug1.wall_to_right = False
        # front-left IR
        if ir_value[1] < 1000:
            wall_follow_bug1.wall_to_left = True
        else:
            if wall_follow_bug1.wall_to_left:
                wall_follow_bug1.previously_wall_to_left = True
                wall_follow_bug1.previously_wall_to_right = False
            wall_follow_bug1.wall_to_left = False

    if bug1.state == Bug1_State.line_follow and wall_in_front:
        bug1.prev_state = bug1.state
        bug1.state = Bug1_State.get_parallel_to_wall
        is_rotating = True

        # set rotate_final_degree
        rotation_dir = choice(['left', 'right'])
        rotation_dir = 'left'
        # rotation_dir = 'right'
        if rotation_dir == 'left':
            rotate_final_degree = (robot_heading + 90) % 360
        else:
            rotate_final_degree = (robot_heading - 90) % 360


def bug1():
    global wall_in_front

    global is_rotating

    global gps_values
    global compass_val
    global sonar_value
    global encoder_value
    global ir_value

    if bug1.state == Bug1_State.reached_destination or bug1.state == Bug1_State.cannot_reach_destination:
        return

    gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()
    
    setup()


    if bug1.state == Bug1_State.init:
        if motion_bug1.head_to_destination(robot_heading, gps_values, final_controller.goal_position):
            bug1.prev_state = bug1.state
            bug1.state = Bug1_State.line_follow
    elif bug1.state == Bug1_State.line_follow:
        motion_bug1.move_forward()
    elif bug1.state == Bug1_State.get_parallel_to_wall:
        if rotation_dir == 'left':
            done = motion_bug1.inplace_rotate(robot_heading, rotate_final_degree, -1)
        else:
            done = motion_bug1.inplace_rotate(robot_heading, rotate_final_degree)
        if done:
            wall_in_front = False
            is_rotating = False
            if rotation_dir == 'left':
                wall_follow_bug1.wall_to_right = True
            else:
                wall_follow_bug1.wall_to_left = True
            bug1.prev_state = bug1.state
            bug1.state = Bug1_State.wall_follow_bug1
    elif bug1.state == Bug1_State.wall_follow_bug1:
        wall_follow_bug1.wall_follow()

    elif bug1.state == Bug1_State.reached_destination:
        update_motor_speed(input_omega=[0, 0, 0])

    # print('sonar: ', sonar_value)
    # print('ir: ', ir_value)
    print(bug1.state)
    print('heading: ', robot_heading)
    print('wall left: ', wall_follow_bug1.wall_to_left)
    print('wall right: ', wall_follow_bug1.wall_to_right)
    print('wall front: ', wall_in_front)
    print('prev wall left: ', wall_follow_bug1.previously_wall_to_left)
    print('prev wall right: ', wall_follow_bug1.previously_wall_to_right)
    print('bug is rot: ', is_rotating)
    print('wall_f is rot: ', wall_follow_bug1.is_rotating)
    print("GPS data: ", gps_values)
    
    update_least_distance()

    # print('left ir: ', ir_value[1])
    print('-----')


bug1.state = Bug1_State.init
bug1.prev_state = Bug1_State.init

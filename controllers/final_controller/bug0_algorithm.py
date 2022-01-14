from random import choice
from enum import Enum

import sense
from initialization import *
import motion
from sense import *
import wall_follow_bug0
import final_controller


class Bug0_State(Enum):
    init = 1
    line_follow = 2
    get_upright = 3
    get_parallel_to_wall = 4
    wall_follow = 5
    finalizing = 6
    reached_destination = 7
    cannot_reach_destination = 8


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

rotate_final_degree = None
rotation_dir = None
# NEVER update stuff when robot is rotating
is_rotating = False


def setup():
    global rotation_dir
    global rotate_final_degree
    global is_rotating

    global wall_in_front

    global robot_heading
    robot_heading = get_bearing_in_degrees(compass_val)

    # check if we've reached the goal
    dist = sense.calculate_distance_to_goal(gps_values, final_controller.goal_position)
    if dist < 0.1:
        rotate_final_degree = 180
        bug0.state = Bug0_State.finalizing
        return

    # NEVER update stuff when robot is rotating
    if not is_rotating and not wall_follow_bug0.is_rotating:
        # any wall around?
        wall_in_front = avoid_wall_in_front(sonar_value[1], ir_value[0], ir_value[3])
        # front-right IR
        if ir_value[5] < 1000:
            wall_follow_bug0.wall_to_right = True
        else:
            if wall_follow_bug0.wall_to_right:
                wall_follow_bug0.previously_wall_to_right = True
                wall_follow_bug0.previously_wall_to_left = False
            wall_follow_bug0.wall_to_right = False
        # front-left IR
        if ir_value[1] < 1000:
            wall_follow_bug0.wall_to_left = True
        else:
            if wall_follow_bug0.wall_to_left:
                wall_follow_bug0.previously_wall_to_left = True
                wall_follow_bug0.previously_wall_to_right = False
            wall_follow_bug0.wall_to_left = False

    if bug0.state == Bug0_State.line_follow and wall_in_front:
        bug0.prev_state = bug0.state
        bug0.state = Bug0_State.get_upright
        is_rotating = True

        # set rotate_final_degree
        # rotation_dir = choice(['left', 'right'])
        # rotation_dir = 'left'
        # rotation_dir = 'right'
        # ######## beautiful case #########
        # if rotation_dir is None:
        #     rotation_dir = 'left'
        # elif rotation_dir == 'left':
        #     rotation_dir = 'right'
        # else:
        #     rotation_dir = 'left'
        # ################################
        # if rotation_dir == 'left':
        #     rotate_final_degree = (robot_heading + 90) % 360
        # else:
        #     rotate_final_degree = (robot_heading - 90) % 360


def bug0():
    global wall_in_front

    global is_rotating

    global gps_values
    global compass_val
    global sonar_value
    global encoder_value
    global ir_value
    global rotation_dir
    global rotate_final_degree

    if bug0.state == Bug0_State.reached_destination:
        return True
    elif bug0.state == Bug0_State.cannot_reach_destination:
        return False

    gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()

    setup()

    if bug0.state == Bug0_State.finalizing:
        if motion.inplace_rotate(robot_heading, rotate_final_degree):
            bug0.state = Bug0_State.reached_destination

    if bug0.state == Bug0_State.init:
        if motion.head_to_destination(robot_heading, gps_values, final_controller.goal_position):
            bug0.prev_state = bug0.state
            bug0.state = Bug0_State.line_follow
    elif bug0.state == Bug0_State.line_follow:
        motion.move_forward()
    elif bug0.state == Bug0_State.get_upright:
        if robot_heading >= 315 or robot_heading < 45:
            if robot_heading < 45:
                got_upright = motion.inplace_rotate(robot_heading, 0)
            else:
                got_upright = motion.inplace_rotate(robot_heading, 0, -1)
            print('0')
        elif 45 <= robot_heading < 135:
            if robot_heading >= 90:
                got_upright = motion.inplace_rotate(robot_heading, 90)
            else:
                got_upright = motion.inplace_rotate(robot_heading, 90, -1)
            print('90')
        elif 135 <= robot_heading < 225:
            if robot_heading >= 180:
                got_upright = motion.inplace_rotate(robot_heading, 180)
            else:
                got_upright = motion.inplace_rotate(robot_heading, 180, -1)
            print('180')
        elif 225 <= robot_heading < 315:
            if robot_heading >= 270:
                got_upright = motion.inplace_rotate(robot_heading, 270)
            else:
                got_upright = motion.inplace_rotate(robot_heading, 270, -1)
            print('270')

        if got_upright:
            ######## beautiful case #########
            if rotation_dir is None:
                rotation_dir = 'left'
            elif rotation_dir == 'left':
                rotation_dir = 'right'
            else:
                rotation_dir = 'left'
            ################################
            if rotation_dir == 'left':
                rotate_final_degree = (robot_heading + 90) % 360
            else:
                rotate_final_degree = (robot_heading - 90) % 360
            bug0.state = Bug0_State.get_parallel_to_wall

    elif bug0.state == Bug0_State.get_parallel_to_wall:
        is_rotating = True
        if rotation_dir == 'left':
            done = motion.inplace_rotate(robot_heading, rotate_final_degree, -1)
        else:
            done = motion.inplace_rotate(robot_heading, rotate_final_degree)
        if done:
            wall_in_front = False
            is_rotating = False
            if rotation_dir == 'left':
                wall_follow_bug0.wall_to_right = True
            else:
                wall_follow_bug0.wall_to_left = True
            bug0.prev_state = bug0.state
            bug0.state = Bug0_State.wall_follow
    elif bug0.state == Bug0_State.wall_follow:
        wall_follow_bug0.wall_follow()

    # print('sonar: ', sonar_value)
    # print('ir: ', ir_value)
    print(bug0.state)
    print('heading: ', robot_heading)
    print('wall left: ', wall_follow_bug0.wall_to_left)
    print('wall right: ', wall_follow_bug0.wall_to_right)
    print('wall front: ', wall_in_front)
    print('prev wall left: ', wall_follow_bug0.previously_wall_to_left)
    print('prev wall right: ', wall_follow_bug0.previously_wall_to_right)
    print('bug is rot: ', is_rotating)
    print('wall_f is rot: ', wall_follow_bug0.is_rotating)
    print('rotation_dir', rotation_dir)
    # print('left ir: ', ir_value[1])
    print('-----')


bug0.state = Bug0_State.init
bug0.prev_state = Bug0_State.init

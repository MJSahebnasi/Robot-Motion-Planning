from random import choice
from enum import Enum

import initialization
import sense
from initialization import *
import motion
from sense import *
import wall_follow
import final_controller


class Bug2_State(Enum):
    init = 1
    line_follow = 2
    get_parallel_to_wall = 3
    wall_follow = 4
    finalizing = 5
    reached_destination = 6
    cannot_reach_destination = 7


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

# distance to goal, when first seeing a wall
primary_hit_distance = 0
last_hit_pos = None
# distance to goal, when leaving the wall
new_leave_distance = 0
line_m = None


def back_on_line():
    thresh = 0.05

    y = gps_values[1]
    x = gps_values[0]
    y0 = final_controller.initial_position[1]
    x0 = final_controller.initial_position[0]

    if line_m == math.inf:
        return abs(x - x0) < thresh

    return abs((y - y0) - line_m * (x - x0)) < thresh


def setup():
    global rotation_dir
    global rotate_final_degree
    global is_rotating

    global wall_in_front

    global robot_heading
    robot_heading = get_bearing_in_degrees(compass_val)

    global primary_hit_distance
    global new_leave_distance
    global line_m
    global last_hit_pos

    # check if we've reached the goal
    dist = sense.calculate_distance_to_goal(gps_values, final_controller.goal_position)
    if dist < 0.1:
        rotate_final_degree = 180
        bug2.state = Bug2_State.finalizing
        return

    # set line_m
    if line_m is None:
        dx = final_controller.goal_position[0] - final_controller.initial_position[0]
        if dx == 0:
            line_m = math.inf
        else:
            line_m = (final_controller.goal_position[1] - final_controller.initial_position[1]) / dx

    # NEVER update stuff when robot is rotating
    if not is_rotating and not wall_follow.is_rotating:
        # any wall around?
        wall_in_front = avoid_wall_in_front(sonar_value[1], ir_value[0], ir_value[3])
        # front-right IR
        if ir_value[5] < 1000:
            wall_follow.wall_to_right = True
        else:
            if wall_follow.wall_to_right:
                wall_follow.previously_wall_to_right = True
                wall_follow.previously_wall_to_left = False
            wall_follow.wall_to_right = False
        # front-left IR
        if ir_value[1] < 1000:
            wall_follow.wall_to_left = True
        else:
            if wall_follow.wall_to_left:
                wall_follow.previously_wall_to_left = True
                wall_follow.previously_wall_to_right = False
            wall_follow.wall_to_left = False

    if bug2.state == Bug2_State.line_follow and wall_in_front:
        bug2.prev_state = bug2.state
        bug2.state = Bug2_State.get_parallel_to_wall
        is_rotating = True

        # calculate distance to goal
        primary_hit_distance = sense.calculate_distance_to_goal(gps_values, final_controller.goal_position)
        last_hit_pos = gps_values[0:2]
        # set rotate_final_degree
        # rotation_dir = choice(['left', 'right'])
        # rotation_dir = 'left'
        # rotation_dir = 'right'

        ######## beautiful case #########
        if rotation_dir is None:
            rotation_dir = 'left'
        elif rotation_dir == 'left':
            rotation_dir = 'right'
        else:
            rotation_dir = 'left'
        ###############################

        if rotation_dir == 'left':
            rotate_final_degree = (robot_heading + 90) % 360
        else:
            rotate_final_degree = (robot_heading - 90) % 360

    if bug2.state == Bug2_State.wall_follow and (
            math.sqrt((gps_values[0] - last_hit_pos[0]) ** 2 + (
                    gps_values[1] - last_hit_pos[1]) ** 2) >= 0.3):

        if back_on_line():
            new_leave_distance = sense.calculate_distance_to_goal(gps_values, final_controller.goal_position)

            if new_leave_distance <= primary_hit_distance:
                bug2.prv_state = bug2.state
                bug2.state = Bug2_State.init

                # clear things
                is_rotating = False
                wall_follow.is_rotating = False
                wall_follow.is_blind = False
                wall_follow.wall_to_right = False
                wall_follow.wall_to_left = False
                wall_follow.previously_wall_to_right = False
                wall_follow.previously_wall_to_left = False
            else:
                print('Cannot reach the goal')
                initialization.update_motor_speed([0, 0, 0])
                bug2.state = Bug2_State.cannot_reach_destination


def bug2():
    global wall_in_front

    global is_rotating

    global gps_values
    global compass_val
    global sonar_value
    global encoder_value
    global ir_value

    global finalizing

    if bug2.state == Bug2_State.reached_destination:
        return True
    elif bug2.state == Bug2_State.cannot_reach_destination:
        return False

    gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()

    setup()

    if bug2.state == Bug2_State.finalizing:
        if motion.inplace_rotate(robot_heading, rotate_final_degree):
            bug2.state = Bug2_State.reached_destination

    if bug2.state == Bug2_State.init:
        if motion.head_to_destination(robot_heading, gps_values, final_controller.goal_position):
            bug2.prev_state = bug2.state
            bug2.state = Bug2_State.line_follow
            # wall_follow.previously_wall_to_right = wall_follow.previously_wall_to_left = False
    elif bug2.state == Bug2_State.line_follow:
        motion.move_forward()
    elif bug2.state == Bug2_State.get_parallel_to_wall:
        if rotation_dir == 'left':
            done = motion.inplace_rotate(robot_heading, rotate_final_degree, -1)
        else:
            done = motion.inplace_rotate(robot_heading, rotate_final_degree)
        if done:
            wall_in_front = False
            is_rotating = False
            if rotation_dir == 'left':
                wall_follow.wall_to_right = True
            else:
                wall_follow.wall_to_left = True
            bug2.prev_state = bug2.state
            bug2.state = Bug2_State.wall_follow
    elif bug2.state == Bug2_State.wall_follow:
        wall_follow.wall_follow()

    # print('sonar: ', sonar_value)
    # print('ir: ', ir_value)
    print(bug2.state)
    # print('heading: ', robot_heading)
    print('wall left: ', wall_follow.wall_to_left)
    print('wall right: ', wall_follow.wall_to_right)
    print('wall front: ', wall_in_front)
    print('prev wall left: ', wall_follow.previously_wall_to_left)
    print('prev wall right: ', wall_follow.previously_wall_to_right)
    # print('bug is rot: ', is_rotating)
    # print('wall_f is rot: ', wall_follow.is_rotating)
    # print('left ir: ', ir_value[1])
    print('-----')


bug2.state = Bug2_State.init
bug2.prev_state = Bug2_State.init

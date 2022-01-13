from enum import Enum

import bug2_algorithm
import motion


class Near_Left_Wall_State(Enum):
    middle = 1
    too_far = 2
    too_close = 3

near_left_wall_state = None

class Near_Right_Wall_State(Enum):
    middle = 1
    too_far = 2
    too_close = 3

near_right_wall_state = None

wall_to_right = False
wall_to_left = False
previously_wall_to_right = False
previously_wall_to_left = False

# NEVER update stuff when robot is rotating
is_rotating = False
rotate_final_degree = None
is_blind = False

first_blindness_position = None


def variable_setup():
    global rotate_final_degree
    global is_rotating
    global near_left_wall_state
    global near_right_wall_state

    global first_blindness_position
    global is_blind

    # NEVER update stuff when robot is rotating
    if not is_rotating:
        if bug2_algorithm.wall_in_front and wall_to_left:
            # rotation_dir = 'right'
            rotate_final_degree = (bug2_algorithm.robot_heading - 90) % 360
        if bug2_algorithm.wall_in_front and wall_to_right:
            # rotation_dir = 'left'
            rotate_final_degree = (bug2_algorithm.robot_heading + 90) % 360
        if not is_blind and not (bug2_algorithm.wall_in_front or wall_to_left or wall_to_right):
            if previously_wall_to_left:
                # rotation_dir = 'left'
                rotate_final_degree = (bug2_algorithm.robot_heading + 90) % 360
            elif previously_wall_to_right:
                # rotation_dir = 'left'
                rotate_final_degree = (bug2_algorithm.robot_heading - 90) % 360
            else:
                for i in range(15):
                    print('da hell?')
        elif bug2_algorithm.wall_in_front and not (wall_to_left or wall_to_right):
            if previously_wall_to_left:
                # rotation_dir = 'right'
                rotate_final_degree = (bug2_algorithm.robot_heading - 20) % 360
            elif previously_wall_to_right:
                # rotation_dir = 'left'
                rotate_final_degree = (bug2_algorithm.robot_heading + 20) % 360
            else:
                for i in range(15):
                    print('da hell? #2')

        left_front_ir_value = bug2_algorithm.ir_value[1]
        if left_front_ir_value < 1000:
            if left_front_ir_value > 450:
                near_left_wall_state = Near_Left_Wall_State.too_far
            elif 450 >= left_front_ir_value >= 400:
                near_left_wall_state = Near_Left_Wall_State.middle
            else:
                near_left_wall_state = Near_Left_Wall_State.too_close

        right_front_ir_value = bug2_algorithm.ir_value[5]
        if right_front_ir_value < 1000:
            if right_front_ir_value > 450:
                near_right_wall_state = Near_Right_Wall_State.too_far
            elif 450 >= right_front_ir_value >= 400:
                near_right_wall_state = Near_Right_Wall_State.middle
            else:
                near_right_wall_state = Near_Right_Wall_State.too_close


"""assumes robot is already parallel to wall and state is set to "follow_wall" """


def wall_follow():
    global wall_to_right
    global wall_to_left
    global previously_wall_to_right
    global previously_wall_to_left

    global is_rotating
    global is_blind
    global rotate_final_degree

    global near_left_wall_state
    global near_right_wall_state

    variable_setup()

    if not bug2_algorithm.wall_in_front and wall_to_left:
        print('follow left wall')
        is_rotating = False
        bug2_algorithm.is_rotating = False
        if near_left_wall_state == Near_Left_Wall_State.middle:
            motion.move_forward()
        elif near_left_wall_state == Near_Left_Wall_State.too_close:
            motion.move_forward_little_to_right()
        elif near_left_wall_state == Near_Left_Wall_State.too_far:
            motion.move_forward_little_to_left()
    elif not bug2_algorithm.wall_in_front and wall_to_right:
        print('follow right wall')
        is_rotating = False
        bug2_algorithm.is_rotating = False
        if near_right_wall_state == Near_Right_Wall_State.middle:
            motion.move_forward()
        elif near_right_wall_state == Near_Right_Wall_State.too_close:
            motion.move_forward_little_to_left()
        elif near_right_wall_state == Near_Right_Wall_State.too_far:
            motion.move_forward_little_to_right()
    elif bug2_algorithm.wall_in_front and wall_to_left:
        print('inplace right')
        is_rotating = True
        done = motion.inplace_rotate(bug2_algorithm.robot_heading, rotate_final_degree)
        bug2_algorithm.is_rotating = True

        if done:
            is_rotating = False
            bug2_algorithm.is_rotating = False
            bug2_algorithm.wall_in_front = False
            previously_wall_to_right = False
            previously_wall_to_left = True
            # wall_to_right = False
            # wall_to_left = True

    elif bug2_algorithm.wall_in_front and wall_to_right:
        print('inplace left')
        is_rotating = True
        done = motion.inplace_rotate(bug2_algorithm.robot_heading, rotate_final_degree, -1)
        bug2_algorithm.is_rotating = True

        if done:
            is_rotating = False
            bug2_algorithm.is_rotating = True
            bug2_algorithm.wall_in_front = False
            previously_wall_to_right = True
            previously_wall_to_left = False
            # wall_to_right = True
            # wall_to_left = False

    elif not (bug2_algorithm.wall_in_front or wall_to_left or wall_to_right):
        print('blind')
        is_blind = True
        # is_rotating = True
        done = False
        print('rot final deg', rotate_final_degree)
        print('heading', bug2_algorithm.robot_heading)
        if previously_wall_to_right:
            done = motion.turn_corner_right(rotate_final_degree)
        elif previously_wall_to_left:
            done = motion.turn_corner_left(rotate_final_degree)

        if done:
            is_blind = False
            # is_rotating = False

    elif bug2_algorithm.wall_in_front and not (wall_to_left or wall_to_right):
        if previously_wall_to_left:
            motion.inplace_rotate(bug2_algorithm.robot_heading, rotate_final_degree)
        else:
            motion.inplace_rotate(bug2_algorithm.robot_heading, rotate_final_degree, -1)


wall_follow.state = None

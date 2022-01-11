from enum import Enum

import bug2_algorithm
import motion


class Near_Wall_State(Enum):
    parallel = 1
    too_far = 2
    too_close = 3


near_wall_state = None

wall_to_right = False
wall_to_left = False
previously_wall_to_right = False
previously_wall_to_left = False

# NEVER update stuff when robot is rotating
is_rotating = False
rotate_final_degree = None


def variable_setup():
    global rotate_final_degree
    global is_rotating
    global near_wall_state

    # NEVER update stuff when robot is rotating
    if not is_rotating:
        if bug2_algorithm.wall_in_front and wall_to_left:
            # rotation_dir = 'right'
            rotate_final_degree = (bug2_algorithm.robot_heading - 90) % 360
        if bug2_algorithm.wall_in_front and wall_to_right:
            # rotation_dir = 'left'
            rotate_final_degree = (bug2_algorithm.robot_heading + 90) % 360
        if not bug2_algorithm.wall_in_front and not (wall_to_left or wall_to_right):
            rotate_final_degree = (bug2_algorithm.robot_heading + 180) % 360
        left_fron_ir_value = bug2_algorithm.ir_value[1]
        if left_fron_ir_value < 1000:
            if left_fron_ir_value > 450:
                near_wall_state = Near_Wall_State.too_far
            elif left_fron_ir_value <= 450 and left_fron_ir_value >= 400:
                near_wall_state = Near_Wall_State.parallel
            else:
                near_wall_state = Near_Wall_State.too_close
        


"""assumes robot is already parallel to wall and state is set to "follow_wall" """


def wall_follow():
    global wall_to_right
    global wall_to_left
    global previously_wall_to_right
    global previously_wall_to_left

    global is_rotating
    global rotate_final_degree

    global near_wall_state

    variable_setup()

    if not bug2_algorithm.wall_in_front and (wall_to_left or wall_to_right):
        # todo
        # move_parallel_to_wall_in_a_more_efficient_way()
        if near_wall_state == Near_Wall_State.parallel:
            motion.move_forward()
        elif near_wall_state == Near_Wall_State.too_close:
            motion.move_forward_little_to_right()
        elif near_wall_state == Near_Wall_State.too_far:
            motion.move_forward_little_to_left()
    elif bug2_algorithm.wall_in_front and wall_to_left:
        # BUG: todo
        # this code needs separate state and execution parts as well
        # cannot set rotate_final_degree every time
        is_rotating = True
        done = motion.inplace_rotate(bug2_algorithm.robot_heading, rotate_final_degree)
        bug2_algorithm.is_rotating = True

        if done:
            is_rotating = False
            bug2_algorithm.is_rotating = False
            bug2_algorithm.wall_in_front = False
            previously_wall_to_right = False
            previously_wall_to_left = True
            wall_to_right = False
            wall_to_left = True

    elif bug2_algorithm.wall_in_front and wall_to_right:
        is_rotating = True
        done = motion.inplace_rotate(bug2_algorithm.robot_heading, rotate_final_degree)
        bug2_algorithm.is_rotating = True

        if done:
            is_rotating = False
            bug2_algorithm.is_rotating = True
            bug2_algorithm.wall_in_front = False
            previously_wall_to_right = True
            previously_wall_to_left = False
            wall_to_right = True
            wall_to_left = False

    elif not bug2_algorithm.wall_in_front and not (wall_to_left or wall_to_right):
        is_rotating = True
        done = False
        if previously_wall_to_right:
            done = motion.turn_corner_right(rotate_final_degree)
        elif previously_wall_to_left:
            done = motion.turn_corner_left(rotate_final_degree)

        if done:
            is_rotating = False
            if previously_wall_to_right:
                wall_to_right = True
            elif previously_wall_to_left:
                wall_to_left = True
            else:
                for i in range(15):
                    print('da hell?')


wall_follow.state = None

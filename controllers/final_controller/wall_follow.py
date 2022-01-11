import bug2_algorithm
import motion

wall_to_right = False
wall_to_left = False
previously_wall_to_right = False
previously_wall_to_left = False

rotate_final_degree = None

"""assumes robot is already parallel to wall"""


def wall_follow():
    global wall_to_right
    global wall_to_left
    global previously_wall_to_right
    global previously_wall_to_left

    global rotate_final_degree

    if not bug2_algorithm.wall_in_front and (wall_to_left or wall_to_right):
        # todo
        # move_parallel_to_wall_in_a_more_complicated_way()
        motion.move_forward()
    elif bug2_algorithm.wall_in_front and wall_to_left:
        # rotation_dir = 'right'
        rotate_final_degree = (bug2_algorithm.robot_heading - 90) % 360
        # BUG:
        # this code needs separate state and execution parts as well
        # cannot set rotate_final_degree every time
        done = motion.inplace_rotate(bug2_algorithm.robot_heading, rotate_final_degree)
        bug2_algorithm.is_rotating = True

        if done:
            bug2_algorithm.is_rotating = False
            bug2_algorithm.wall_in_front = False
            previously_wall_to_right = False
            previously_wall_to_left = True
            wall_to_right = False
            wall_to_left = True
    elif bug2_algorithm.wall_in_front and wall_to_right:
        # rotation_dir = 'left'
        rotate_final_degree = (bug2_algorithm.robot_heading + 90) % 360

        done = motion.inplace_rotate(bug2_algorithm.robot_heading, rotate_final_degree)
        bug2_algorithm.is_rotating = True

        if done:
            bug2_algorithm.is_rotating = True
            bug2_algorithm.wall_in_front = False
            previously_wall_to_right = True
            previously_wall_to_left = False
            wall_to_right = True
            wall_to_left = False
    elif not bug2_algorithm.wall_in_front and not (wall_to_left or wall_to_right):
        if previously_wall_to_right:
            motion.turn_corner_right()
        elif previously_wall_to_left:
            motion.turn_corner_left()

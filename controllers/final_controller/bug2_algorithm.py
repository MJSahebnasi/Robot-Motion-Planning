from initialization import *
from motion import *
from sense import *

goal_position = np.array([1.3, 6.15])  # <x,y>
initial_position = np.array([1.3, -9.74])

threshold = 0.08
# head: sonar[1], ir[0], ir[3]

robot_heading = None

wall_in_front = False
wall_to_right = False
wall_to_left = False

gps_values = None
compass_val = None
sonar_value = None
encoder_value = None
ir_value = None

rotate_final_degree = None
rotation_dir = None


def set_state():
    global wall_in_front
    global wall_to_right
    global wall_to_left

    global rotation_dir
    global rotate_final_degree

    wall_in_front = avoid_wall_in_front(sonar_value[1])

    if bug2.state == 'line_follow' and wall_in_front:
        bug2.prev_state = bug2.state
        bug2.state = 'get_parallel_to_wall'

        # set rotate_final_degree
        rotation_dir = choice(['left', 'right'])
        if rotation_dir == 'left':
            rotate_final_degree = (robot_heading - 90) % 360
        else:
            rotate_final_degree = (robot_heading + 90) % 360


def bug2():
    global wall_in_front
    global wall_to_right
    global wall_to_left

    global gps_values
    global compass_val
    global sonar_value
    global encoder_value
    global ir_value

    gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()

    global robot_heading
    robot_heading = get_bearing_in_degrees(compass_val)

    if not bug2.state == 'init':
        set_state()

    if bug2.state == 'init':
        if head_to_destination(robot_heading, gps_values, goal_position):
            bug2.prev_state = bug2.state
            bug2.state = 'line_follow'
    elif bug2.state == 'line_follow':
        move_forward()
    elif bug2.state == 'get_parallel_to_wall':
        if rotation_dir == 'left':
            inplace_rotate(robot_heading, rotate_final_degree)
        else:
            inplace_rotate(robot_heading, rotate_final_degree, -1)


bug2.state = 'init'
bug2.prev_state = 'init'

from initialization import *
from motion import *
from sense import *

goal_position = np.array([1.3, 6.15])  # <x,y>
initial_position = np.array([1.3, -9.74])

threshold = 0.08


# head: sonar2, ir1, ir4

def bug2():
    gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()

    wall_in_front = avoid_wall_in_front(sonar_value[1])

    if bug2.state == 'init':
        if head_to_destination(get_bearing_in_degrees(compass_val), gps_values, goal_position):
            bug2.state = 'line_follow'
    elif bug2.state == 'line_follow' and not wall_in_front:
        move_forward()



bug2.state = 'init'

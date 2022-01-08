import numpy as np
import math


def get_bearing_in_degrees(compass_val):
    rad = np.arctan2(compass_val[0], compass_val[1])
    bearing = (rad - 1.5708) / math.pi * 180.0

    return bearing + 270

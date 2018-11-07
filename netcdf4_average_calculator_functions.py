import netCDF4
import numpy as np

#numpy provides an averaging method for numpy arrays, but I wanted to demonstrate the logic below.
def calculate_average(numpy_array):
    total_value = np.float32(0.0)
    number_of_values = np.int(0)
    for value in np.nditer(numpy_array):
        total_value += value
        number_of_values += np.int(1)
    return np.float32(total_value / number_of_values)

#Not currently used.
#Could be utilized to implement logic to skip a value when calculating an average.
def detect_invalid_value(actual_value, valid_min, valid_max, missing_value):
    if actual_value < valid_min or actual_value > valid_max or actual_value ==  missing_value:
        return True
    else:
        return False

#Not currently used.
#Could be utilized to implement logic to skip a value when calculating an average.
def detect_invalid_delta(first_value, second_value, valid_delta):
    if abs(first_value - second_value) > valid_delta:
        return True
    else:
        return False

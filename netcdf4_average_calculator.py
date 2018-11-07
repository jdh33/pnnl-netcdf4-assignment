import os
import sys
import glob
import netCDF4
import numpy as np
from netcdf4_average_calculator_functions import *

#This interval is used for averaging values in the input variables. The original values are from readings
#every 60 seconds, so to average readings for every 5 minutes we need to use 5 values.
#60 seconds * 5 = 300 seconds = 5 minutes
AVERAGING_INDEX_INTERVAL = 5

for input_file in glob.glob('input/*.cdf'):

    output_file = input_file.replace('input', 'output')
    output_file = output_file.replace('met', 'metavg')

    input_dataset = netCDF4.Dataset(input_file)
    output_dataset = netCDF4.Dataset(output_file, 'w', format = 'NETCDF3_CLASSIC')

    #initialize netCDF4 varialbes for output files using time as a dimension
    #using the same numpy float32 type used in the input files
    time = output_dataset.createDimension('time', None)
    atmospheric_pressure = output_dataset.createVariable('atmospheric_pressure', np.float32(), ('time',))
    mean_temperature =  output_dataset.createVariable('mean_temperature', np.float32(), ('time',))

    #All variables associated with atmosphere readings are at index 0
    #All variables associated with temperature readings are at index 1
    list_of_input_netcdf4_variables = [input_dataset['atmos_pressure'], input_dataset['temp_mean']]
    list_of_output_netcdf4_variables = [atmospheric_pressure, mean_temperature]

    #The variable_index corresponds to a specific variable of interest
    #len(list_of_output_netcdf4_variables) is equal to the number of variables to iterate through
    variable_index = 0
    while variable_index < len(list_of_output_netcdf4_variables):
        netcdf4_variable = list_of_output_netcdf4_variables[variable_index]
        #slice the entire netCDF4 variable retrieved to convert it into a numpy array
        np_array = list_of_input_netcdf4_variables[variable_index][:]
        average_values = np.array([], dtype = np.float32)

        #These indexes are used to slice 5 values at a time, which corresonds to 5 minutes
        subarray_start_index = 0
        subarray_end_index = subarray_start_index + AVERAGING_INDEX_INTERVAL
        while (subarray_start_index < len(np_array)):
            average = np.float32(0.0)
            #Python will automatically slice to the last element if the subarray_end_index
            #is greater than the last index value.
            #A warning could be implemented if the last averaged value is the not for the desired interval.
            average = calculate_average(np_array[subarray_start_index:subarray_end_index])
            average_values = np.append(average_values, average)

            #Shift the indexes so the next group of values can be averaged.
            subarray_start_index += AVERAGING_INDEX_INTERVAL
            subarray_end_index += AVERAGING_INDEX_INTERVAL

        #Get the names of the attributes ("the medadata") associated with the varialbe.
        names_of_variable_attributes = list_of_input_netcdf4_variables[variable_index].ncattrs()
        #The same metadata used in the input file will be used for the output file for each variable.
        for attribute_name in names_of_variable_attributes:
            attribute_value = list_of_input_netcdf4_variables[variable_index].getncattr(attribute_name)
            list_of_output_netcdf4_variables[variable_index].setncattr(attribute_name, attribute_value)

        #This is setting a variable in the output netCDF4 file the average values.
        list_of_output_netcdf4_variables[variable_index][:] = average_values

        variable_index += 1

    input_dataset.close()
    output_dataset.close()

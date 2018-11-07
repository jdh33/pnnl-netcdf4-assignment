import unittest
import numpy as np
import netCDF4
import netcdf4_average_calculator_functions as net_funtions

class NetCDF4AverageCalculatorFunctionsTest(unittest.TestCase):

    def setUp(self):
        self.short_numpy_array = np.array([1.0, 2.0])
        self.long_numpy_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 20.0])

    #Check the averaging funciton with various arrays and array slices.
    def test_calculate_average(self):

        #Use slicing to simulate averaging over a time interval.
        self.assertEqual(net_funtions.calculate_average(self.short_numpy_array[0:5]), np.float32(1.5))
        self.assertNotEqual(net_funtions.calculate_average(self.short_numpy_array[0:5]), np.float32(1.51))
        self.assertEqual(net_funtions.calculate_average(self.long_numpy_array[0:5]), np.float32(3.0))
        self.assertEqual(net_funtions.calculate_average(self.long_numpy_array[5:10]), np.float32(15.0))

#Compare manually entered attributes to retrieved attributes
class NetCDF4AverageCalculatorAttributesComparisonTest(unittest.TestCase):

    def setUp(self):
        self.test_atmos_pressure_attribute_names = ['long_name', 'units', 'valid_min', 'valid_max', 'valid_delta', 'missing_value']
        self.test_atmos_pressure_attribute_values = ['Atmospheric pressure', 'kPa', np.float32(80.0), np.float32(110.0), np.float32(1.0), np.float32(-9999.0)]
        self.test_temp_mean_attribute_names = ['long_name', 'units', 'valid_min', 'valid_max', 'valid_delta', 'missing_value']
        self.test_temp_mean_attribute_values = ['Temperature mean', 'degC', np.float32(-40.0), np.float32(50.0), np.float32(20.0), np.float32(-9999.0)]

        self.test_data_set = netCDF4.Dataset('test_files/test_input_file.cdf')

    def tearDown(self):
        self.test_data_set.close()

    #Manually check that the correct attributes ("metadata") are retrieved
    def test_metadata_retrieval(self):
        #Get variables from a file.
        atmos_pressure = self.test_data_set.variables['atmos_pressure']
        temp_mean = self.test_data_set.variables['temp_mean']

        #Get attributes
        atmos_pressure_attribute_names = atmos_pressure.ncattrs()
        atmos_pressure_attribute_values = []
        for attribute_name in atmos_pressure_attribute_names:
            atmos_pressure_attribute_values.append(atmos_pressure.getncattr(attribute_name))

        temp_mean_attribute_names = temp_mean.ncattrs()
        temp_mean_attribute_values = []
        for attribute_name in temp_mean_attribute_names:
            temp_mean_attribute_values.append(temp_mean.getncattr(attribute_name))

        self.assertCountEqual(self.test_atmos_pressure_attribute_names, atmos_pressure_attribute_names)
        self.assertCountEqual(self.test_atmos_pressure_attribute_values, atmos_pressure_attribute_values)
        self.assertCountEqual(self.test_temp_mean_attribute_names, temp_mean_attribute_names)
        self.assertCountEqual(self.test_temp_mean_attribute_values, temp_mean_attribute_values)

if __name__ == '__main__':
    unittest.main(verbosity=2)

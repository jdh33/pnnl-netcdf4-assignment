# pnnl-netcdf4-assignment

Objective:  Using python create a script that reads the time-series data in the provided NetCDF4 files and creates daily files with time intervals of 5 minutes.

Details:  Create a python program that uses the NetCDF4 files available in this link to create a corresponding NetCDF4 files.  The values of the variables in output file should be 5 minute averages of variables ‘atmos_pressure’ and ‘temp_mean’ from the input NetCDF4 files.  The new output file names should replace ‘met’ in the original file name to ‘metavg’.   The variables should be renamed as ‘atmospheric_pressure’ and ‘mean_temperature’ and any relevant metadata/data related to these variables should be propagated to the output file. Provide the link to your git repository that includes your source code and all five NetCDF output files. Provide at least two unit tests that can be run with pytest to validate your results.

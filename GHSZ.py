# -----------------------------------------------
# Name: Gas Hydrate Stability Zone
# Version: 0.1.0 // Oct 2019
# Purpose: Calculate the base of the hydrate stability zone from the sea floor
# Author: James M Roden
# Created: Oct 2019
# ArcGIS Version: 10.5
# Dependencies: NumPy 1.7.1
# Python Version 2.6
# PEP8
# -----------------------------------------------

from __future__ import division
import arcpy
import numpy as np
import math
import os
import sys
import traceback


class IncorrectRasterStats(Exception):
    pass


# Joides Formula function
def joides(water_depth, base_water_temp, geothermal_gradient):
    """Returns the base of the gas hydrate stability zone for a given water depth

    Joides formula for calculating the base gas hydrate stability meters below sea floor. As per the publication:
    Ocean Drilling Program Guidelines for Pollution Prevention and Safety; JOIDES Journal, Volume 18, Special Issue
    No. 7, October 1992.
    A range of 1-2501 is used, as per studies, generally the maximum is 2000 meters below surface.


    Args:
        water_depth: The absolute value of the water depth in meters
        base_water_temp: Bottom water temperature in degrees celsius
        geothermal_gradient: Geothermal gradient in degrees celsius/kilometers
    """

    if water_depth in memoize_dict:  # memoization for speed up
        return memoize_dict[water_depth]  # memoization for speed up
    else:
        for z in range(1, 2501):
            a = math.log((10.17 * (water_depth + z)))
            if a > 9.355001:
                for z2 in range(1, 2501):
                    a2 = math.log((10.17 * (water_depth + z2)))
                    b2 = 46.74 - (10748.1 / ((base_water_temp + ((z2 * geothermal_gradient) / 1000)) + 273.15))
                    if a2 < b2:
                        memoize_dict[water_depth] = z2  # memoization for speed up
                        return z2
            else:
                b = 38.53 - (8386.8 / ((base_water_temp + (z * geothermal_gradient / 1000)) + 273.15))
                if a < b:
                    memoize_dict[water_depth] = z  # memoization for speed up
                    return z

# Memoization dictionary for water depth/z
memoize_dict = {}

try:
    # ArcGIS environment
    arcpy.env.workspace = "in_memory"
    arcpy.env.scratchWorkspace = "in_memory"
    arcpy.env.overwriteOutput = True

    # ArcGIS Tool Parameters
    in_raster = arcpy.GetParameterAsText(0)
    in_water_temp = arcpy.GetParameter(1)
    in_geo_gradient = arcpy.GetParameter(2)
    workspace = arcpy.GetParameterAsText(3)

    # Raster information
    in_raster = arcpy.Raster(in_raster)

    if in_raster.minimum < 0 or in_raster.maximum < 0:
        raise IncorrectRasterStats

    lower_left = in_raster.extent.lowerLeft
    cell_width = in_raster.meanCellWidth
    cell_height = in_raster.meanCellHeight
    sr = in_raster.spatialReference

    # Array manipulation
    in_array = arcpy.RasterToNumPyArray(in_raster, nodata_to_value=99999)
    in_array = in_array.astype(int)  # Convert to int for performance
    vectorised_joides = np.vectorize(joides)
    out_array = vectorised_joides(in_array, in_water_temp, in_geo_gradient)

    # Out Raster
    no_data_value = joides(99999, in_water_temp, in_geo_gradient)  # Reverse calculate no data value
    out_raster = arcpy.NumPyArrayToRaster(out_array, lower_left, cell_width, cell_height, no_data_value)

    # Define raster and save output
    final_output = os.path.join(workspace, "GHSZ_Output")
    arcpy.CopyRaster_management(out_raster, final_output)
    arcpy.DefineProjection_management(final_output, sr)

except IncorrectRasterStats:
    arcpy.AddError("Error: Raster must be positive.")

except Exception as ex:
    _, error, tb = sys.exc_info()
    traceback_info = traceback.format_tb(tb)[0]
    arcpy.AddError("Error Type: {} \nTraceback: {} \n".format(error, traceback_info))

finally:
    arcpy.Delete_management('in_memory')
    arcpy.AddMessage("in_memory intermediate files deleted.")

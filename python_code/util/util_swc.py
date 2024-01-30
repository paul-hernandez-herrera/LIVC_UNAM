import numpy as np
import pandas as pd
from pathlib import Path
from .basic_func import cummulative_euclidian_distance_between_points, read_csv

def read_swc(file_path,file_name):
    full_path = Path(file_path, file_name)
    
    # Attempt to read the CSV file with a standard comma delimiter
    swc = pd.read_csv(full_path , header = None).values
    
    # Check if the shape of the array is not [n, 7]
    if swc.shape[1]!=7:
        # If unsuccessful, attempt to read the CSV file with custom settings
        swc = pd.read_csv(full_path , header = None, comment='#', delim_whitespace = True).values
        
        # Check if the shape is still not [n, 7]
        if swc.shape[1]!=7:
            raise Exception("Could not read SWC file. Check if the file exists and its shape is [n,7].")
    return swc

def write_swc(file_name, array):
    df = pd.DataFrame(array)
    
    df[0] = df[0].astype(int)
    df[1] = df[1].astype(int)
    df[6] = df[6].astype(int)
    df.to_csv(file_name, index=False, header = None, float_format='%.4f')
   

def points_to_swc(points):
    n_rows = points.shape[0]
    swc = np.column_stack((np.arange(n_rows), np.zeros((n_rows, 5)), np.arange(n_rows)-1))
    swc[0, 6] = -1
    swc[:, 2:5] = points
    
    return swc

def interpolate_swc(swc, n_points = 0, interpolation_type = "linear"):
    # function to convert any swc file to a fixed number of points
    
    points = swc[:,2:5]
    
    n_points = n_points or swc.shape[0]
        
    x = cummulative_euclidian_distance_between_points(points)
    
    x_new = np.linspace(0, x[-1], num = n_points)
    
    new_points = np.zeros((n_points,3))
    if interpolation_type=="linear":
        new_points[:,0] = np.interp(x_new, x, points[:,0])
        new_points[:,1] = np.interp(x_new, x, points[:,1])
        new_points[:,2] = np.interp(x_new, x, points[:,2])
        
    
    swc = points_to_swc(new_points)
        
    return swc

def swc_to_micron(file_swc, file_txt, file_output = ""):
    # function to convert swc file to micrometers
    spacing_xy = 118/640    
    file_swc = Path(file_swc)
    
    swc, z_micron = read_swc(file_swc.parent, file_swc.name), read_csv(file_txt).flatten()
    
    # we have to substract 1, because matlab index start at 1, while python at 0
    swc[:, 4] = np.clip(swc[:, 4], None, len(z_micron)) -1
    
    
    swc[:, 4] = z_micron[swc[:, 4].astype(int)]
    swc[:, 2:4] = spacing_xy * swc[:, 2:4]
    
    output_path = Path(file_output) if Path(file_output).suffix == ".swc" else Path(file_output, file_swc.stem + "_micron.swc")
    
    if file_output:
        write_swc(output_path, swc)      
    
    return swc
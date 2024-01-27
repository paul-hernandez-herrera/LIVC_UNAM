import numpy as np
import pandas as pd
from pathlib import Path
from .basic_func import cummulative_euclidian_distance_between_points, read_csv

def read_swc(file_path,file_name):
    return np.array(pd.read_csv(Path(file_path, file_name) , header = None, comment='#', delim_whitespace = True))

def points_to_swc(points):
    n_rows = points.shape[0]
    swc = np.column_stack((np.arange(n_rows), np.zeros((n_rows, 5)), np.arange(n_rows)+1))
    swc[0, -1] = -1
    swc[:, 2:5] = points
    
    return swc

def smooth_swc(swc, n_points = 0, interpolation_type = "linear"):
    # function to convert any swc file to a fixed number of points
    
    points = swc[:,2:5]
    
    n_points = n_points or swc.shape[0]
        
    x = cummulative_euclidian_distance_between_points(points)
    
    x_new = np.linspace(0, x[-1], num = n_points)
    
    new_points = np.zeros(n_points,3)
    if interpolation_type=="linear":
        new_points[:,0] = np.interp(x_new, x, points[:,0])
        new_points[:,1] = np.interp(x_new, x, points[:,1])
        new_points[:,2] = np.interp(x_new, x, points[:,2])
        
    
    swc = points_to_swc(new_points)
        
    return swc

def swc_to_micron(file_swc, file_txt, folder_output = None):
    # function to convert swc file to micrometers
    spacing_xy = 118/640    
    file_swc = Path(file_swc)
    
    swc, z_micron = read_swc(file_swc.parent, file_swc.name), read_csv(file_txt).flatten()
    
    # we have to substract 1, because matlab index start at 1, while python at 0
    swc[:, 4] = np.clip(swc[:, 4], None, len(z_micron)) -1
    
    
    swc[:, 4] = z_micron[swc[:, 4]]
    swc[:, 2:4] = spacing_xy * swc[:, 2:4]
    
    return swc
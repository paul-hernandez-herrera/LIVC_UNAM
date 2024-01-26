import numpy as np
import pandas as pd
from pathlib import Path
from basic_func import cummulative_euclidian_distance_between_points

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
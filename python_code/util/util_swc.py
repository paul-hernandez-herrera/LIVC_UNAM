import numpy as np
import pandas as pd
from pathlib import Path

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
    
    if n_points == 0:
        n_points = swc.shape[0]
        
    time = cummulative_euclidian_distance_between_points(points)
    
    time_new = np.linspace(0, time[-1], num = n_points)
    if interpolation_type=="linear":
        x_new = np.interp(time_new, time, points[:,0])
        y_new = np.interp(time_new, time, points[:,1])
        z_new = np.interp(time_new, time, points[:,2])
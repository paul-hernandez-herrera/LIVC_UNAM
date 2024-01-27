import tifffile
from pathlib import Path
import skimage.io as io
import pandas as pd
import numpy as np

def cummulative_euclidian_distance_between_points(points):
    # we assume that coordinates of points are given in the rows
    cum_dist = np.zeros(points.shape[0],)
    cum_dist[1:] = np.cumsum(np.sqrt(np.sum(np.power(np.diff(points, axis=0),2), axis = 1)))
    
    return cum_dist

def imread(filename):
    if Path(filename).suffix.lower() in {'.tif', '.tiff'}:
        return tifffile.imread(filename)
    if Path(filename).suffix.lower() in {'.mhd'}:
        return io.imread(filename, plugin='simpleitk')
        
def imwrite(filename, arr):
    if Path(filename).suffix.lower() in {'.tif', '.tiff'}:
        tifffile.imsave(filename, arr) 

def read_csv(csv_dataset_file_path):
    #read pandas data frame
    pd_data = pd.read_csv(csv_dataset_file_path, header = None)
    #convert data to numpy array
    data = pd_data.values

    return data

def write_csv(file_name, array):
    df = pd.DataFrame(array)
    df.to_csv(file_name, index=False, header = None)

        




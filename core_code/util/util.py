import tifffile
from pathlib import Path
import skimage.io as io
import pandas as pd
import numpy as np

def imread(filename):
    if Path(filename).suffix.lower() in {'.tif', '.tiff'}:
        return tifffile.imread(filename)
    if Path(filename).suffix.lower() in {'.mhd'}:
        return io.imread(filename, plugin='simpleitk')
        
def imwrite(filename, arr):
    if Path(filename).suffix.lower() in {'.tif', '.tiff'}:
        tifffile.imsave(filename, arr) 
        
        
def get_image_file_paths(input_path):
    input_path = Path(input_path)
    
    # Check if input path is a directory or a file
    if input_path.is_dir():
        img_file_paths  = list(input_path.glob('*.tiff')) + list(input_path.glob('*.tif'))
    elif input_path.suffix in ['.tiff', '.tif']:
        img_file_paths  = [input_path]
    else:
        raise ValueError('Input file format not recognized. Currently only tif files can be processed (.tif or .tiff)')
        
    # Check if any image files were found    
    if not img_file_paths:
        raise ValueError("No .tiff or .tif files found in the given path.")
        
    return img_file_paths    

def read_swc(file_path,file_name):
    return np.array(pd.read_csv(Path(file_path, file_name) , header = None, comment='#', delim_whitespace = True))

def write_csv(file_name, array):
    df = pd.DataFrame(array)
    df.to_csv(file_name, index=False, header = None)

def create_file_in_case_not_exist(folder_path):
    folder_path.mkdir(parents=True, exist_ok=True)
    return


    
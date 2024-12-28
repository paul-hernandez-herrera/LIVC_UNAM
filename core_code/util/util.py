import tifffile
from pathlib import Path
import skimage.io as io
import pandas as pd
import numpy as np

def imread(filename):
    if Path(filename).suffix.lower() in {'.tif', '.tiff'}:
        return tifffile.imread(filename)
    if Path(filename).suffix.lower() in {'.mhd'}:
        return read_mhd_and_raw(filename)
        
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

def read_mhd_and_raw(mhd_file):
    """
    Lee un stack 3D desde archivos MHD y RAW.

    Parameters:
        mhd_file (str): Ruta al archivo .mhd.

    Returns:
        numpy.ndarray: Volumen 3D cargado.
    """
    # Leer metadatos del archivo .mhd
    header = {}
    with open(mhd_file, 'r') as f:
        for line in f:
            parts = line.strip().split(' = ')
            if len(parts) == 2:
                key, value = parts
                header[key.strip()] = value.strip()
    
    # Extraer información relevante
    raw_file = header.get('ElementDataFile')  # Nombre del archivo .raw
    dim_size = list(map(int, header['DimSize'].split()))  # Tamaño del volumen
    element_type = header['ElementType']  # Tipo de dato
    element_spacing = list(map(float, header['ElementSpacing'].split()))  # Espaciado
    
    # Mapear el tipo de dato de MetaImage a NumPy
    type_mapping = {
        'MET_UCHAR': np.uint8,
        'MET_CHAR': np.int8,
        'MET_USHORT': np.uint16,
        'MET_SHORT': np.int16,
        'MET_UINT': np.uint32,
        'MET_INT': np.int32,
        'MET_FLOAT': np.float32,
        'MET_DOUBLE': np.float64,
    }
    
    dtype = type_mapping.get(element_type)
    if dtype is None:
        raise ValueError(f"Tipo de elemento no soportado: {element_type}")
    
    # Leer el archivo .raw
    raw_file_path = mhd_file.rsplit('/', 1)[0] + '/' + raw_file  # Asumimos que .raw está junto al .mhd
    volume = np.fromfile(raw_file_path, dtype=dtype).reshape(dim_size[::-1])
    
    return volume


    
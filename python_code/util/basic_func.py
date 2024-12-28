import tifffile
from pathlib import Path
import skimage.io as io
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def cummulative_euclidian_distance_between_points(points):
    # we assume that coordinates of points are given in the rows
    cum_dist = np.zeros(points.shape[0],)
    cum_dist[1:] = np.cumsum(np.sqrt(np.sum(np.power(np.diff(points, axis=0),2), axis = 1)))
    
    return cum_dist

def imread(filename):
    file_name = Path(filename)
    valid_suffixes = {'.tif', '.tiff', '.mhd'}
    
    if file_name.suffix.lower() not in valid_suffixes:
        for suffix in ['.mhd', '.tif', '.tiff']:
            if file_name.with_suffix(suffix).exists():
                file_name = file_name.with_suffix(suffix)
                break
    
    suffix = file_name.suffix.lower()
    if suffix in {'.tif', '.tiff'}:
        return tifffile.imread(file_name)
    elif suffix == '.mhd':
        return read_mhd_and_raw(file_name)
        
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
    
def create_folder_in_case_not_exist(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    return

def create_cell_array(shape):
    shape = np.array(shape)
    
    n_entries = shape.prod()
    temp = []
    cell_array = np.array([temp.append([]) for _ in range(n_entries)], dtype=object).reshape(shape)
    return cell_array

def points_get_PCA_components(X):
    pca = PCA();
    pca.fit(X)
    return(pca.components_)

def rodrigues_rotation(v, k, theta):
    # https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    k = k/np.linalg.norm(k)
    
    v = np.array(v)
    
    v_rot = (v*np.cos(theta)) + (np.cross(k,v)*np.sin(theta)) + (k*(np.dot(k,v)*(1.0-np.cos(theta))))
            
    return(v_rot)
        
def read_mhd_and_raw(mhd_file):
    """
    Lee un stack 3D desde archivos MHD y RAW.

    Parameters:
        mhd_file (str): Ruta al archivo .mhd.

    Returns:
        numpy.ndarray: Volumen 3D cargado.
    """
    
    mhd_file = Path(mhd_file)
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
    raw_file_path = Path(mhd_file.parent,mhd_file.stem + ".raw")  # Asumimos que .raw está junto al .mhd
    volume = np.fromfile(raw_file_path, dtype=dtype).reshape(dim_size[::-1])
    
    return volume



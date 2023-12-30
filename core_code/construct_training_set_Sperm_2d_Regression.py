import numpy as np
from pathlib import Path
import pandas as pd
from .util import util

def create_training_set(csv_file_path, folder_output, img_size = 128, n = 3):
    #read pandas data frame
    dataset = Dataset_spermNeck(csv_file_path)

    for i in range(len(dataset)):
        path_img, path_swc = dataset.__getitem__(i)

        img3D, swc = util.imread(path_img), util.read_swc(path_swc.parent, path_swc.name)

        img2D = preprocess_stack(img3D)
        
        neck_point = np.array([swc[0,3], swc[0,2]])
        #generate training set random position [-32,32]
        for j in range(n-1):
            random_displacement = np.random.randint(low = -32, high=32, size=(1,2), dtype=int)
            left_upper_corner = neck_point - (img_size//2) + random_displacement

            img_cropped, left_upper_corner = crop_subvolumes_2D(img2D, left_upper_corner, img_size)

            file_name_base = Path(folder_output, str(i))
            util.write_csv(file_name_base.with_suffix(".csv"), neck_point-left_upper_corner)
            util.imwrite(file_name_base.with_suffix(".tif"), img_cropped)    


def preprocess_stack(img3D):
    # We assume that image shape is [Depth, Width, Height]

    # percentile normalization
    low = np.percentile(img3D[:], 0.01)
    high = np.percentile(img3D[:], 99.99)
    img3D = np.clip(img3D, low, high)

    # zero mean and one varianza
    img3D = (img3D - np.mean(img3D[:])) / np.std(img3D[:])

    # maximum intensity projection
    img3D = np.max(img3D, axis=0)

    return img3D

def crop_subvolumes_2D(img, left_upper_corner, v_size):
    v_size = np.int_(v_size)
       
    # check good boundary conditions
    img_shape = img.shape
    left_upper_corner = np.maximum(np.int_(left_upper_corner), 0)
    left_upper_corner = np.minimum(left_upper_corner, img_shape - v_size)     
            
    img_cropped = img[left_upper_corner[0,0]:left_upper_corner[0,0]+v_size, left_upper_corner[0,1]:left_upper_corner[0,1]+v_size]
    
    return img_cropped, left_upper_corner


class Dataset_spermNeck():
    def __init__(self, csv_file_path):
        dataFrame = pd.read_csv(csv_file_path)

        self.current_traces_paths = []
        self.current_images_paths = []

        ## getting swc and images paths
        for idx in range(dataFrame.shape[0]):
            traces_paths = [p for p in Path(dataFrame.iloc[idx, 1]).iterdir() if p.suffix == ".swc"]
            if not traces_paths:
                raise Exception(f"{dataFrame.iloc[idx, 1]} does not have any trace (*.swc file).")

            self.current_traces_paths.extend(traces_paths)
            self.current_images_paths.extend(self.get_image_for_trace(dataFrame.iloc[idx, 0], p) for p in traces_paths)
        

    def __len__(self):
        return len(self.current_traces_paths)
    
    def __getitem__(self, idx):
        return self.current_images_paths[idx], self.current_traces_paths[idx]

    def get_image_for_trace(self, folder_image, trace_path):
        file_name = Path(trace_path).stem
        n1, n2 = file_name.find("_TP"), file_name.find("_raw")
        file_ID, num_stack = file_name[0:n1], int(file_name[n1+3:n2])

        for num_digits in [3, 4]:
            image_file_name = f"{file_ID}_TP{num_stack:0{num_digits}}"
            image_path_mhd, image_path_tif = Path(folder_image, image_file_name + ".mhd"), Path(folder_image, image_file_name + ".tif")
            
            if image_path_mhd.is_file() or image_path_tif.is_file():
                return image_path_mhd if image_path_mhd.is_file() else image_path_tif
        
        raise Exception(f"{trace_path} does not have any associated image.")
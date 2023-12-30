import numpy as np
from pathlib import Path
import pandas as pd
from .util import util
import csv
from tqdm import tqdm

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


class construct_training_set():
    
    def __init__(self):
        self.set_default_values()

        
    def set_default_values(self):
        #Default values for the class
        self.patch_size_img = 256
        self.number_patches = 3        
        return 

    def run_main(self):
        self.core()
        
        
        
    ## PRIVATE METHODS
    def core(self):
        # brighfield
        # we assume the organization of the data is:
        # input_images:---- /.../folder1/*.mhd
        # traces:---- /.../folder1/folder_sub/*.saw
        
        if not self.folder_output:
            self.folder_output = Path(self.folder_imgs, 'training_set')
        
        print(f'folder_output: {self.folder_output}')
        folders_subdir = self.list_subdirs(self.folder_imgs)        
        list_training_set = self.__verify_correct_traninig_set(folders_subdir)
        
        
        #make output folders
        folder_out_imgs = Path(self.folder_output, 'input')
        folder_out_masks = Path(self.folder_output, 'target')
        [self.__create_folder_if_not_exist(path) for path in (self.folder_output, folder_out_imgs, folder_out_masks)]

        count_img = 0
        n_files = len(list_training_set)
        
        data_csv = []
        for index, file_paths in enumerate(tqdm(list_training_set)):
            #print(f'Running stack: {index + 1}/{n_files}')
            #print(file_paths[0])
            img, swc = self.__get_data(file_paths)
            
            #preprocess_data
            img = preprocess_image(img, percentile_range = [self.norm_perc_low, self.norm_perc_high], normalization_range = [0,1] )
            img = np.squeeze(img)
            
            #generate the ground true as a tubular structure
            mask = self.construct_tubular_mask(np.array(img.shape), swc, self.radius_tubular_mask)
            
            if self.draw_head:
                swc_head = swc[0:1,:]
                mask = mask | self.construct_tubular_mask(np.array(img.shape), swc_head , int(2.5*self.radius_tubular_mask))
            
            #generate training set images containing the flagellum
            for i in np.random.choice(swc.shape[0], self.number_patches, replace=False):
                left_upper_corner = swc[i,3:1:-1] - self.patch_size_img/2
                #random shift of the left-corner
                left_upper_corner += np.random.randint(low = -self.patch_size_img/4, high=self.patch_size_img/4, size=2, dtype=int)
                img_cropped, mask_cropped = self.__crop_subvolumes(img, mask, left_upper_corner, self.patch_size_img)
                io.imwrite(Path(folder_out_imgs, f"img_{count_img:06}.tif"), img_cropped)
                io.imwrite(Path(folder_out_masks, f"img_{count_img:06}.tif"), mask_cropped)
                data_csv.append([f"img_{count_img:06}.tif", file_paths[0], file_paths[1], left_upper_corner[0], left_upper_corner[1], self.patch_size_img])
                count_img+=1

            #generate training set images containing the flagellum
            for i in range(0, self.number_patches_random_pos):
                left_upper_corner = np.array([np.random.randint(low = self.patch_size_img, high=img.shape[1]- self.patch_size_img, size=1, dtype=int)[0],
                                              np.random.randint(low = self.patch_size_img, high=img.shape[2]- self.patch_size_img, size=1, dtype=int)[0]])
                img_cropped, mask_cropped = self.__crop_subvolumes(img, mask, left_upper_corner, self.patch_size_img)
                io.imwrite(Path(folder_out_imgs, f"img_{count_img:06}.tif"), img_cropped)
                io.imwrite(Path(folder_out_masks, f"img_{count_img:06}.tif"), mask_cropped)
                data_csv.append([f"img_{count_img:06}.tif",file_paths[0], file_paths[1], left_upper_corner[0], left_upper_corner[1], self.patch_size_img])
                count_img+=1                


        with open(Path(self.folder_output,'training_set_imgs_info.csv'), "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_csv)
        print('------------------------------')
        print('\033[47m' '\033[1m' 'Algorithm has finished generating training set.' '\033[0m')
        print('------------------------------')  
        print('\nTraining set saved in path: ')
        print(self.folder_output)
        print('\n')
        
    def __create_folder_if_not_exist(self, folder_path):
        folder_path.mkdir(parents=True, exist_ok=True)
        
    def __crop_subvolumes(self, img, mask, left_upper_corner, v_size):    
        #check good boundary conditions
        left_upper_corner = np.int_(left_upper_corner)
        v_size = np.int_(v_size)
        
        left_upper_corner[left_upper_corner<0] = 0
        
        #check the subvolume does not fall outside the img.shape
        img_2d_shape = np.array([img.shape[1],img.shape[2]])
        outside_index = (left_upper_corner+ v_size)>img_2d_shape
        left_upper_corner[outside_index] = img_2d_shape[outside_index] - v_size      
                
        
        img_cropped = img[:,left_upper_corner[0]:left_upper_corner[0]+ v_size,left_upper_corner[1]:left_upper_corner[1]+v_size]
        mask_cropped = mask[:,left_upper_corner[0]:left_upper_corner[0]+ v_size,left_upper_corner[1]:left_upper_corner[1]+v_size]
        
        #make sure to have a fixed size in z-axis. For brightfield data 45 images is the average size
        img_cropped = self.convert_img_to_shape(img_cropped, np.array([45, img_cropped.shape[1], img_cropped.shape[2]]))
        mask_cropped = self.convert_img_to_shape(mask_cropped, np.array([45, mask_cropped.shape[1], mask_cropped.shape[2]]))
        
        return img_cropped, mask_cropped    
 
    
    def __get_data(self, file_paths):
        swc = io.read_swc(file_paths[0].parent, file_paths[0].name)
        img = io.imread(file_paths[1])
        
        return img, swc
    

    

    
    def convert_img_to_shape(self, img, new_shape):
        old_shape = img.shape
        
        temp_shape = np.maximum(old_shape,new_shape)
        
        new_img = np.full(temp_shape, np.amin(img), dtype = img.dtype)
        
        new_img[0:old_shape[0], 0:old_shape[1], 0:old_shape[2]] = img
        
        return new_img[0:new_shape[0], 0:new_shape[1], 0:new_shape[2]]
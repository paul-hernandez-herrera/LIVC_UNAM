import numpy as np
from pathlib import Path
from .util import util as io
import csv
from .util.preprocess import preprocess_image
from tqdm import tqdm

#from . import util

class construct_training_set():
    
    def __init__(self):
        self.set_default_values()

        
    def set_default_values(self):
        #Default values for the class
        self.folder_traces = ''
        self.folder_imgs = ''
        self.folder_output = ''
        self.patch_size_img = 128
        self.number_patches = 10
        self.number_patches_random_pos = 2
        self.radius_tubular_mask = 4
        self.norm_perc_low = 1
        self.norm_perc_high = 99
        self.draw_head = True
        self.file_names = []
        
        return 

    def set_number_patches_random_pos(self, val):
        self.number_patches_random_pos = val
        return        

    def set_folder_traces(self, val):
        self.folder_traces = Path(val)
        return

    def set_folder_imgs(self, val):
        self.folder_imgs = Path(val)
        return
    
    def set_folder_output(self,val):
        self.folder_output = Path(val)
        return    
        
    def set_patch_size_img(self, val):
        self.patch_size_img = val
        return
        
    def set_number_patches(self, val):
        self.number_patches = val
        return
        
    def set_radius_tubular_mask(self, val):
        self.radius_tubular_mask = val
        return

    def set_normalization_percentile_low(self, val):
        self.norm_perc_low = val
        return

    def set_normalization_percentile_high(self, val):
        self.norm_perc_high = val
        return

    def set_draw_head(self, val):
        self.draw_head = val
        return

    def percentile_normalization(self, img, p_low, p_high):
        #normalize data to percentile and [0,1]
        low = np.percentile(img, p_low)
        high = np.percentile(img, p_high)
        
        normalize_img = (np.clip(img, low, high) - low)/(high-low)
        return normalize_img

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
        
    def list_subdirs(self, root_dir):
        list_dir = [f for f in Path(root_dir).iterdir() if f.is_dir()]
        output = []
        for f in list_dir:
            output = self.list_subdirs(f) + output
        return list_dir + output

        
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
    
    def construct_tubular_mask(self, img_shape, swc, r):
        #create a larger volume to have good boundary conditions
        cylinder_mask = np.full(img_shape+2*r, False)
        
        sphere = self.__construct_sphere(r)
        for i in range(0, swc.shape[0]):
            #updating coordinates
            x, y, z = swc[i,2:5]-1
            self.__merge_volumes(cylinder_mask, sphere, np.uint16(np.array([z,y,x])))
            
        return np.uint8(cylinder_mask[r:r+img_shape[0],r:r+img_shape[1],r:r+img_shape[2]]>0)
    
    def __construct_sphere(self, r):
        c = np.arange(-r,r+1)
        
        Z, X, Y = np.meshgrid(c,c,c)
        
        dist_ = np.sqrt(X**2 + Y**2 + Z**2)
        
        return dist_<=r
    
    def __merge_volumes(self, large_vol, small_vol, ini_pos):
        #We assume that small_volume is inside large volume (It is satisfied by construction)
        large_vol[ini_pos[0]:ini_pos[0]+small_vol.shape[0], ini_pos[1]:ini_pos[1]+small_vol.shape[1], ini_pos[2]:ini_pos[2]+small_vol.shape[2]] =  large_vol[ini_pos[0]:ini_pos[0]+small_vol.shape[0], ini_pos[1]:ini_pos[1]+small_vol.shape[1], ini_pos[2]:ini_pos[2]+small_vol.shape[2]] | small_vol
        return large_vol
    
    def __verify_correct_traninig_set(self, list_subdir):
        pairs_files = []
        #verify each image has the corresponding swc trace
        for folder in list_subdir:
            swc_file_names = [p for p in folder.iterdir() if p.suffix in {'.swc'}]
            img_file_names = [p for p in list(folder.iterdir())+ list(folder.parent.iterdir()) if p.suffix in {'.mhd'}]
            for swc_path in swc_file_names:
                swc_stem = swc_path.stem
                breaking = False
                for img_path in img_file_names:
                    img_stem = img_path.stem
                    if img_stem in swc_stem:
                        if img_path.suffix in {'mhd'} and not(Path(img_path.parent, img_stem + '.raw').exist()):
                            raise Exception(f'Missing raw files for trace {swc_path}')        
                        pairs_files.append([swc_path, img_path])
                        breaking = True
                        break
                if not breaking:
                    raise Exception(f'Missing img files for trace {swc_path}')
        return pairs_files
    
    def convert_img_to_shape(self, img, new_shape):
        old_shape = img.shape
        
        temp_shape = np.maximum(old_shape,new_shape)
        
        new_img = np.full(temp_shape, np.amin(img), dtype = img.dtype)
        
        new_img[0:old_shape[0], 0:old_shape[1], 0:old_shape[2]] = img
        
        return new_img[0:new_shape[0], 0:new_shape[1], 0:new_shape[2]]
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:49:56 2024

@author: paulh
"""
from python_code.util import  basic_func, util_swc, preprocess
import numpy as np
from pathlib import Path
import torch

def predict_3D_stack(image, model, device='cpu', flag_preprocess = True):
    """
    Predict a 3D image stack using a PyTorch model.

    Args:
        image (np.ndarray): Input 3D image with shape [D, H, W] or [C, D, H, W].
        model (torch.nn.Module): PyTorch model for prediction.
        device (str, optional): Device to run the prediction on ('cpu' or 'cuda'). Default is 'cpu'.

    Returns:
        np.ndarray: Probability map scaled to [0, 255] with the same shape as the input image.
    """
    model.eval()
    # Disable gradient computation to save memory and improve performance
    with torch.no_grad():
        # Ensure the input image is in float32 format for consistency
        input_image = image.astype(float)

        # Preprocess the image to normalize its intensity
        if flag_preprocess:
            input_image = preprocess.preprocess_3d_stack_for_AI_segmentation(input_image)

        # Convert the preprocessed image to a PyTorch shape [B,C,D,W,H] -> [1,1,D,W,H] tensor and move it to the specified device
        tensor_image = torch.tensor(input_image).float().unsqueeze(0).unsqueeze(0).to(device=device)

        # Pass the tensor through the model to obtain the network's raw output
        raw_output = model(tensor_image)

        # Apply a sigmoid activation function to obtain probabilities (values in [0, 1]) and map it back to shape [D, W, H]
        probability_map = torch.sigmoid(raw_output).squeeze().squeeze().cpu().numpy()

    # Scale the probabilities to [0, 255] for visualization or further processing
    return (255 * probability_map).astype(np.uint8)


class construct_training_set():
    
    def __init__(self, folder_traces, folder_images, folder_output, 
                 patch_size = [-1,96,96], radius = 2, n_patch_foreground = 10, n_patch_random = 2, draw_head = True):
        self.folder_output = Path(folder_output)
        self.patch_size = np.array(patch_size)
        self.radius = radius
        self.n_patch_foreground = n_patch_foreground
        self.n_patch_random = n_patch_random
        self.draw_head = draw_head
        
        # Este es el código principal que permite identificar las imágenes y trazas 
        # necesarias para construir el conjunto de entrenamiento del modelo.
        # -----------------------------------------------------------------------------
        
        self.dataset = []  # Lista para almacenar pares de rutas (trazado, imagen)
        
        # Crear pares de rutas (archivo de traza, imagen asociada)
        for trace_folder, image_folder in zip(folder_traces, folder_images): 
            # Iterar sobre los archivos en la carpeta de entrada y filtrar los archivos .swc
            for trace_file in Path(trace_folder).iterdir():
                if trace_file.suffix == '.swc':  # Considerar solo archivos .swc
                    # Construir las rutas completas del trazado y su imagen asociada
                    image_path = Path(image_folder, trace_file.stem + ".mhd")
                    trace_path = Path(trace_folder, trace_file.name)
                    self.dataset.append([image_path, trace_path])  # Añadir al conjunto de datos
        
        # Verificar la existencia de la imagen asociada (.mhd)
        for trace_path, image_path in self.dataset:           
            if not image_path.exists():
                raise ValueError(f"Missing image for trace: {trace_path.name}\nRequired file: {image_path}\n")
                
        ######################################################################
        
    ## PRIVATE METHODS
    def run(self):
        """
        Main method for generating training datasets, including preprocessed images
        and masks for AI segmentation, and saving them into designated output folders.
        """               
        
        # Define output folders for images and masks
        output_folder_images  = Path(self.folder_output, 'input')
        output_folder_masks  = Path(self.folder_output, 'target')
        [self.__create_folder_if_not_exist(path) for path in (self.folder_output, output_folder_images, output_folder_masks)]

        image_counter = 0  # Counter for naming saved images and masks
        n_files = len(self.dataset) # Total number of files in the dataset
        
        # Iterate through the dataset files
        for index, files_path in enumerate(self.dataset):
            print(f'Processing stack: {index + 1}/{n_files}')
            
            # Load the 3D image stack and SWC data
            img, swc = self.__get_data(files_path)
            
            # Normalize the 3D image stack intensities to the range [-1, 1]
            img = preprocess.preprocess_3d_stack_for_AI_segmentation(img)
            
            # Generate the ground truth mask as a tubular structure
            ground_truth_mask  = self.construct_tubular_mask(np.array(img.shape), swc, self.radius)
            
            
            # Optionally add a larger mask around the head region
            if self.draw_head:
                swc_head = swc[[0],:]
                head_mask = self.construct_tubular_mask(np.array(img.shape), swc_head , int(5*self.radius))
                ground_truth_mask |= head_mask
            
            # Generate training patches centered around flagellum positions
            flagellum_positions = np.random.choice(swc.shape[0], self.n_patch_foreground, replace=False)
            flagellum_positions = np.append(flagellum_positions, [-1,-1,-1,-1,0])  # Include the flagellum tip and head
            for position_index  in flagellum_positions:
                # Compute the upper-left corner of the patch
                left_upper_corner = swc[position_index ,4:1:-1] - self.patch_size/2
                
                #random shift of the left-corner
                left_upper_corner += np.random.randint(low=-np.array(self.patch_size) // 4, high=np.array(self.patch_size) // 4, size=3, dtype=int)
                
                # Crop sub-volumes of the image and mask
                img_cropped, mask_cropped = self.__crop_subvolumes(img, ground_truth_mask , left_upper_corner, self.patch_size)
                
                # Save the cropped image and mask
                basic_func.imwrite(Path(output_folder_images, f"img_{image_counter:06}.tif"), img_cropped)
                basic_func.imwrite(Path(output_folder_masks, f"img_{image_counter:06}.tif"), mask_cropped)
                image_counter+=1

            # Generate random patches from the 3D stack
            max_coordinate = self.patch_size//2
            
            for _ in range(0, self.n_patch_random):
                # Randomly select the upper-left corner of the patch
                left_upper_corner = np.array([np.random.choice(np.arange(max_coordinate[0], img.shape[0]-max_coordinate[0]+1),1)[0], 
                                              np.random.choice(np.arange(max_coordinate[1], img.shape[1]-max_coordinate[1]+1),1)[0], 
                                              np.random.choice(np.arange(max_coordinate[2], img.shape[2]-max_coordinate[2]+1),1)[0] ])
                
                # Crop sub-volumes of the image and mask
                img_cropped, mask_cropped = self.__crop_subvolumes(img, ground_truth_mask , left_upper_corner, self.patch_size)
                
                # Save the cropped image and mask
                basic_func.imwrite(Path(output_folder_images, f"img_{image_counter:06}.tif"), img_cropped)
                basic_func.imwrite(Path(output_folder_masks, f"img_{image_counter:06}.tif"), mask_cropped)
                image_counter+=1                
                
        print('------------------------------')
        print('\033[47m' '\033[1m' 'Algorithm has finished generating training set.' '\033[0m')
        print('------------------------------')  
        print('\nTraining set saved in path: ')
        print(self.folder_output)
        print('\n')
        
    def __crop_subvolumes(self, img, mask, left_upper_corner, v_size):    
        #check good boundary conditions
        left_upper_corner = np.int_(left_upper_corner)
        v_size = np.int_(v_size)
        
        left_upper_corner[left_upper_corner<0] = 0
        
        #check the subvolume does not fall outside the img.shape
        img_3d_shape = np.array(img.shape)
        outside_index = (left_upper_corner+ v_size)>img.shape
        left_upper_corner[outside_index] = img_3d_shape[outside_index] - v_size[outside_index]
        
        
        img_cropped = img[left_upper_corner[0]:left_upper_corner[0]+ v_size[0],
                          left_upper_corner[1]:left_upper_corner[1]+ v_size[1],
                          left_upper_corner[2]:left_upper_corner[2]+v_size[2]]
        mask_cropped = mask[left_upper_corner[0]:left_upper_corner[0]+ v_size[0], 
                            left_upper_corner[1]:left_upper_corner[1]+ v_size[1], 
                            left_upper_corner[2]:left_upper_corner[2]+v_size[2]]
        
        return img_cropped, mask_cropped    
 
    
    def __get_data(self, files_path):
        img = basic_func.imread(files_path[0])
        swc = util_swc.read_swc(files_path[1].parent, files_path[1].name)
        return img, swc
    
    def construct_tubular_mask(self, img_shape, swc, r):
        #create a larger volume to have good boundary conditions
        cylinder_mask = np.full(img_shape+2*r, False)
        
        sphere = self.__construct_sphere(r)
        
        #### We assume that coordinates are obtained with origin at [1,1,1]. Convertir to Python origin [0,0,0]
        swc[:,2:5] = swc[:,2:5]-1 
        
        for i in range(0, swc.shape[0]):
            #updating coordinates
            x, y, z = swc[i,2:5]
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
    
    def __create_folder_if_not_exist(self, folder_path):
        folder_path.mkdir(parents=True, exist_ok=True)   
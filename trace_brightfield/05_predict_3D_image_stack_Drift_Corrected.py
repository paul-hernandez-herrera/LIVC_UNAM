# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 11:46:33 2024

@author: paulh
"""
'''
Parameters to predict the segmentation for 3D image stacks. 
'''
model_path = r"E:\SPERM\Training_dataset\2024_12_30_flagellum_head_brightfield\modelo_2024_12_30\modelo_UNet_3D_epoch_00009.pth"

folder_images = r"E:\SPERM\Fluorescencia_Campo_Claro\20241210 CC 4000fps Calceina y Fluo 4000fps - 90hz 20 micras\STACKS\Exp7_stacks"
file_prefix = "Exp7_stacks"


import os
if 'workbookDir' not in globals():
    print('Updating working directory')
    workbookDir = os.path.dirname(os.getcwd())
    os.chdir(workbookDir)
    
print(os.getcwd())

from trace_brightfield.util_deep_learning import predict_3D_stack
from trace_brightfield.UNet_3D_model import UNet_3D
from python_code.util import basic_func, preprocess
from pathlib import Path
import torch
import matplotlib.pyplot as plt
import numpy as np

def display_side_by_side_image(input_img, network_output, file_out):

    # Mostrar imágenes lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))  # 1 fila, 2 columnas
    axes[0].imshow(np.max(input_img, axis=0), cmap = 'gray')
    axes[0].axis('off')  # Ocultar ejes
    axes[0].set_title('Input image')
    
    axes[1].imshow(np.max(network_output,axis=0), cmap = 'gray')
    axes[1].axis('off')
    axes[1].set_title('Segmentation')
    
    plt.tight_layout()
    plt.savefig(file_out, bbox_inches='tight') 
    plt.close()

'''
MAIN CODE TO PREDICT IMAGES
'''
    
# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Abrir modelo
modelo1 = UNet_3D().to(device) # Create the model
modelo1.load_state_dict(torch.load(model_path, weights_only=True))

# Abrir modelo
# modelo2 = UNet_3D().to(device) # Create the model
# modelo2.load_state_dict(torch.load(model_path_2, weights_only=True))

folder_img_output = Path(folder_images, "segmentation_jpeg")
folder_img_output.mkdir(parents=True, exist_ok=True)

for timepoint in range(0,1000):
    file_name = f"{file_prefix}_TP{timepoint:04}_DC"
    
    file_img = Path(folder_images, file_name)
    
    if file_img.with_suffix('.mhd').exists() or file_img.with_suffix('.tif').exists():
        print(f"Running prediction for {file_name}")
        input_img = basic_func.imread(Path(folder_images, file_name))
        
        input_img = input_img.astype(float)
        
        input_img = preprocess.preprocess_3d_stack_for_AI_segmentation(input_img)
        
        network_output = predict_3D_stack(input_img, modelo1, device, flag_preprocess = False)
        # network_output_2 = predict_3D_stack(input_img, modelo2, device, flag_preprocess = False)
        
        # network_output = np.maximum(network_output_1, network_output_2)
        
        file_output = file_name+"_segmentation.tif"
        
        basic_func.imwrite(Path(folder_images, file_output), network_output)
        
        display_side_by_side_image(input_img, network_output, Path(folder_img_output, file_name + ".jpeg"))
    






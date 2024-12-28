# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 16:18:53 2024

@author: paulh
"""
import os
from pathlib import Path

# Cambiar el directorio de trabajo
workbookDir = Path(__file__).parent.parent.resolve()
os.chdir(workbookDir)
print(f"Currernt working directory: \n{os.getcwd()}")

from trace_brightfield.util_deep_learning import construct_training_set

# Create the parameters to generate training set.
patch_size = [16,96,96]
radius = 2
n_patch_foreground = 5
n_patch_random = 1

# Set the output path
folder_output = r"E:\SPERM\Training_dataset\2024_12_26_flagellum_head_brightfield"

# Set the input paths (IMGS and SWC)
folder_traces = [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks\trace_voxels_cell_1"]
folder_images = [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks"]

folder_traces += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks\trace_voxels_cell_2"]
folder_images += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks"]

folder_traces += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp8_stacks\trace_voxels"]
folder_images += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp8_stacks"]

folder_traces += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp9_stacks\trace_voxels"]
folder_images += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp9_stacks"]

folder_traces += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp11_stacks\trace_voxels"]
folder_images += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp11_stacks"]

folder_traces += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp13_stacks\trace_voxels"]
folder_images += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp13_stacks"]

folder_traces += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp16_stacks\trace_voxels"]
folder_images += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp16_stacks"]

folder_traces += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp17_stacks\trace_voxels"]
folder_images += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp17_stacks"]
#RUN THE CODE
# Generate and object of class construct_training_set
gen_train = construct_training_set(folder_traces, folder_images, folder_output,
                                   patch_size = patch_size, 
                                   radius = radius,
                                   n_patch_foreground = n_patch_foreground,
                                   n_patch_random = n_patch_random)

# run the code
gen_train.run()



 
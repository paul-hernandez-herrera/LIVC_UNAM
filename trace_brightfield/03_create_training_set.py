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
patch_size = [16,128,128]
radius = 2
n_patch_foreground = 2
n_patch_random = 1

# Set the output path
folder_output = r"E:\SPERM\Training_dataset\2024_12_29_flagellum_head_brightfield"

# Set the input paths (IMGS and SWC)
folder_traces = [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp9_stacks"]
folder_images = [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp9_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp10_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp10_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp12_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp12_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp15_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp15_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp16_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac 6hr 30 Mayo 2017\DONE_Exp16_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac T0 31 Mayo 2017\DONE_Exp3_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac T0 31 Mayo 2017\DONE_Exp3_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac T0 31 Mayo 2017\DONE_EXP10_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170601 NAC Sperm Capac T0 31 Mayo 2017\DONE_EXP10_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp4_stacks\cell1_voxels"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp4_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp6_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp6_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp9_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp9_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp10_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp10_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp12_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170602 NAC Sperm Capac 6hr 2 Junio 2017\DONE_Exp12_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170607 NAC Sperm Capac T0 7Junio 2017\DONE_Exp3_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170607 NAC Sperm Capac T0 7Junio 2017\DONE_Exp3_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170607 NAC Sperm Capac T0 7Junio 2017\DONE_Exp6_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170607 NAC Sperm Capac T0 7Junio 2017\DONE_Exp6_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170607 NAC Sperm Capac T0 7Junio 2017\DONE_Exp7_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170607 NAC Sperm Capac T0 7Junio 2017\DONE_Exp7_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp2_stacks\cell2_voxels"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp2_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp3_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp3_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp9_stacks\cell1_voxels"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp9_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp11_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp11_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp12_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_170815 NAC Sperm Capac 6hr 6 Junio 2017\DONE_Exp12_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp9_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp9_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp10_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp10_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp11_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp11_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp15_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp15_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp17_stacks\voxels1"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_171108 NAC Capac Campo Claro 08 Nov 17\DONE_Exp17_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 6_stacks\cell1_voxels"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 6_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 9_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 9_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 13_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 13_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 14_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 14_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 16_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181026 Capacitados 26 oct 2018\DONE_Exp 16_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 4_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 4_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 7_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 7_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 9_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 9_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 11_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 11_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 15_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181030 Capacitados 30 oct 2018\DONE_Exp 15_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181031 Capacitados 31 oct 2018\DONE_Exp 7_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181031 Capacitados 31 oct 2018\DONE_Exp 7_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181031 Capacitados 31 oct 2018\DONE_Exp 12_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181031 Capacitados 31 oct 2018\DONE_Exp 12_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181031 Capacitados 31 oct 2018\DONE_Exp 20_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181031 Capacitados 31 oct 2018\DONE_Exp 20_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181031 Capacitados 31 oct 2018\DONE_Exp 21_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20181031 Capacitados 31 oct 2018\DONE_Exp 21_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp2_stacks\cell1_voxels"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp2_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp3_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp3_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp5_stacks"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp5_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp7_stacks\cell1_voxels"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp7_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp8_stacks\cell1_voxels"]
folder_images += [r"E:\SPERM\campo_claro\CAPACITADOS\DONE_20190326 Capacitados\DONE_Exp8_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp7_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp7_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp9_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp9_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp13_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp13_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp19_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp19_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp15_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp15_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp2_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp2_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp3_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp3_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp5_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp5_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp12_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp12_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp14_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp14_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp18_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp18_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp22_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp22_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp25_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp25_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp26_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_14_HIGH_VISCOCITY_DONE\2017_11_14_HIGH_VISCOCITY_DONE\Exp26_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp13_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp13_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp2_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp2_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp4_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp4_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp14_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp14_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp15_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp15_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp16_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_16_HIGH_VISCOCITY_DONE\2017_11_16_HIGH_VISCOCITY_DONE\Exp16_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp7_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp7_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp11_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp11_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp16_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp16_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp18_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp18_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp19_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_22_HIGH_VISCOCITY_DONE\2017_11_22_HIGH_VISCOCITY_DONE\Exp19_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp4_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp4_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp10_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp10_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp11_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp11_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp12_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp12_stacks"]

folder_traces += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp16_stacks"]
folder_images += [r"E:\SPERM\campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\2017_11_24_HIGH_VISCOCITY_DONE\Exp16_stacks"]

folder_traces += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks\trace_voxels_cell_1"]
folder_images += [r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks"]

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



 
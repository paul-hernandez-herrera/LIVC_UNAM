import os
workbookDir = os.path.dirname(os.getcwd())
os.chdir(workbookDir)

from util.util_swc import swc_to_micron
from util.basic_func import create_file_in_case_not_exist
from pathlib import Path

folder_path_height_txt = r"C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\Exp11_stacks"
folder_path_swc = r"C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\Exp11_stacks\trace_head_removed\trace_voxels"
folder_output = r"C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\HIGH_VISCOCITY\2017_11_24_HIGH_VISCOCITY_DONE\Exp11_stacks\trace_head_removed\trace_micras"
stack_id = "Exp11_stacks"

create_file_in_case_not_exist(folder_output)

for tp in range(1000):
    file_name = f"{stack_id}_TP{tp:04}"
    file_swc = Path(folder_path_swc, file_name + "_raw.swc")
    file_txt = Path(folder_path_height_txt, file_name + ".txt")
    
    if file_swc.is_file():
        swc_to_micron(file_swc, file_txt, folder_output)
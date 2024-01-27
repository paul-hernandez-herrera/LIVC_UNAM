import os
if 'workbookDir' not in globals():
    workbookDir = os.path.dirname(os.getcwd())
    os.chdir(workbookDir)
    

from head_fixed_frame import raw_traces_parameters_path
from util import basic_func, util_swc

# here we read all the dataset information
file_path_rotations, folder_path_traces, file_id_stack, sperm_id = raw_traces_parameters_path.high_viscocity_information_parameters()

for i in range(len(file_path_rotations)):
    csv_rotation = basic_func.read_csv(file_path_rotations[i])
    tp = csv_rotation[:,0]
    head_spin_angle = csv_rotation[:,1]
    
    swc_file_name = f"{file_id_stack[i]}"
    util_swc.read_swc(folder_path_traces[i], )
    print()
    
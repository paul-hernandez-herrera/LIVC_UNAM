# set current folder as the working directory
import os
workbookDir = os.path.dirname(os.getcwd())
os.chdir(workbookDir)
    
import scipy.io as sio
from head_fixed_frame import raw_traces_parameters_path
from util import  util_swc
from util.basic_func import read_csv, create_cell_array 
from pathlib import Path

# here we read all the dataset information
file_path_rotations, folder_path_traces, file_id_stack, sperm_labels = raw_traces_parameters_path.high_viscocity_information_parameters()
folder_output = r"C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\HIGH_VISCOCITY\data_traces"

n = len(sperm_labels)
sperm_tp_analized = create_cell_array([1,n])
head_spin_angle = create_cell_array([1,n])
trace = create_cell_array([1,n])
sperm_id = create_cell_array([1,n])

for i in range(n):
    print(f"Running {i+1}/{n}")
    csv_rotation = read_csv(file_path_rotations[i])
    current_time_points = csv_rotation[:,0].flatten().astype(int)
    current_head_spin_angle = csv_rotation[:,1]
    
    current_trace = create_cell_array([1, len(current_time_points)])
    for index, tp in enumerate(current_time_points):
        swc_file_name = f"{file_id_stack[i]}_TP{tp:04}_raw_micron.swc"
        swc = util_swc.read_swc(folder_path_traces[i], swc_file_name)
        current_trace[0,index] = swc
    
    sperm_tp_analized[0,i] = current_time_points
    head_spin_angle[0,i] = current_head_spin_angle
    trace[0,i] = current_trace
    sperm_id[0,i] = sperm_labels[i]
    
variables_output = {"sperm_tp_analized": sperm_tp_analized,
                    "head_spin_angle": head_spin_angle,
                    "trace": trace,
                    "sperm_id": sperm_id
    }

sio.savemat(Path(folder_output,  "01_Lab_Frame_High_Viscocity.mat"), variables_output)
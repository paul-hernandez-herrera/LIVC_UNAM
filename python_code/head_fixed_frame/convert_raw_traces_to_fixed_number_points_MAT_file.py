from pathlib import Path
import os    
import scipy.io as sio
from util.util_swc import interpolate_swc
from util.util_vtk import swc_to_vtk_lines
from util.basic_func import create_cell_array, create_file_in_case_not_exist
import numpy as np 

# set current folder as the working directory
workbook_dir = os.path.dirname(Path(__file__).parent.resolve())
os.chdir(workbook_dir)

# here we read all the dataset information
folder_path = r"C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\HIGH_VISCOCITY\data_traces"
file_input_name = "01_Lab_Frame_High_Viscocity_raw.mat"
file_output_name = "01_Lab_Frame_High_Viscocity_raw_fixed_n_points.mat"
n_points = 100
flag_write_vtk = True

# loading input variables
dict_traces = sio.loadmat(Path(folder_path, file_input_name))
traces, tp, sperm_id, head_spin_angle = (
    dict_traces["trace"],
    dict_traces["sperm_tp_analized"],
    dict_traces["sperm_id"],
    dict_traces["head_spin_angle"],
)

# Create output folders if writing VTK files
if flag_write_vtk:
    folder_vtk_output = Path(folder_path, "vtk")
    create_file_in_case_not_exist(folder_vtk_output)
    for n_exp in range(sperm_id.shape[1]):
        create_file_in_case_not_exist( Path(folder_vtk_output, sperm_id[0, n_exp][0]) )     

# Creating variables to save generated data
X, Y, Z = (
    create_cell_array((1, traces.shape[1])),
    create_cell_array((1, traces.shape[1])),
    create_cell_array((1, traces.shape[1])),
)

for n_exp in range(traces.shape[1]):
    current_trace = traces[0,n_exp]
    current_x, current_y, current_z = (
        np.zeros((n_points, current_trace.shape[1])),
        np.zeros((n_points, current_trace.shape[1])),
        np.zeros((n_points, current_trace.shape[1])),
    )
    
    for i in range(current_trace.shape[1]):
        swc = current_trace[0,i]
        new_swc = interpolate_swc(swc, n_points = n_points, interpolation_type = "linear")
        current_x[:,i] = new_swc[:,2]
        current_y[:,i] = new_swc[:,3]
        current_z[:,i] = new_swc[:,4]
        
        if flag_write_vtk:
            swc_to_vtk_lines(Path(folder_vtk_output, sperm_id[0,n_exp][0], f"raw_{tp[0,n_exp][0,i]:04}.vtk"), swc)
            swc_to_vtk_lines(Path(folder_vtk_output, sperm_id[0,n_exp][0], f"raw_fixed_n_points_{tp[0,n_exp][0,i]:04}.vtk"), new_swc)
    X[0, n_exp], Y[0, n_exp], Z[0, n_exp] = current_x, current_y, current_z
            
variables_output = {"head_spin_angle": head_spin_angle,
                    "sperm_id": sperm_id,
                    "sperm_tp_analized": tp,
                    "X": X,
                    "Y": Y,
                    "Z": Z
    }

sio.savemat(Path(folder_path,  file_output_name), variables_output)
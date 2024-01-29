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
folder_path = r"C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\HIGH_VISCOCITY\data_traces"
file_name = "01_Lab_Frame_High_Viscocity_raw.mat"
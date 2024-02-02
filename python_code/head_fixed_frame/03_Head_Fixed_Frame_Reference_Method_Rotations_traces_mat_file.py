# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:34:39 2021

@author: paul
"""
import os
from pathlib import Path
# set current folder as the working directory
workbook_dir = os.path.dirname(Path(__file__).parent.resolve())
os.chdir(workbook_dir)


import scipy.io as sio
import numpy as np
from util.basic_func import create_folder_in_case_not_exist, rodrigues_rotation, write_csv
from util.util_vtk import swc_to_vtk_lines
from pathlib import Path
import sys
from util.util_swc import points_to_swc

flag_automatic_head_spin_rotation = False


def main(argv):
    
    # Input for dataset HIGH_VISCOCITY
    folder_root = r"C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\HIGH_VISCOCITY\data_traces"
    file_labFrame = Path(folder_root, "01_Lab_Frame_High_Viscocity_raw_fixed_n_points.mat")
    file_neck_frame = Path(folder_root, "02_Neck_Frame_High_Viscocity_raw_fixed_n_points_10_um.mat")
    file_head_frame_output_name = Path(folder_root, "03_Head_Fixed_Frame_High_Viscocity_raw_fixed_n_points_head_spin_by_drifraction.mat")
    
    # Create folder to save vtk files    
    folder_root_vtk_output = Path(folder_root, "03_Head_Fixed_Frame")
    create_folder_in_case_not_exist(folder_root_vtk_output)    
    
    #loading data from mat file
    variables_neck_frame = sio.loadmat(file_neck_frame)
    variables_lab_frame = sio.loadmat(file_labFrame)
    
    variables_neck_frame["head_spin_angle_cummulative"] = variables_neck_frame['head_spin_angle'].copy()
    for sp in range(variables_neck_frame['X'].shape[1]):
        sperm_id = variables_neck_frame['sperm_id'][0,sp][0]       
        folder_vtk_output = Path(folder_root_vtk_output, sperm_id)
        create_folder_in_case_not_exist(folder_vtk_output)
        
        # traces in Neck Fixed Frame for sperm sp 
        X_neck = variables_neck_frame['X'][0, sp]
        Y_neck = variables_neck_frame['Y'][0, sp]
        Z_neck = variables_neck_frame['Z'][0, sp]        
        time_points = variables_neck_frame['sperm_tp_analized'][0,sp]
        head_spin_angle = variables_neck_frame['head_spin_angle'][0, sp][0,:]
        
        head_spin_angle_cummulative = convert_head_spin_from_range_0_90_to_full_rotations_0_360(head_spin_angle)
        variables_neck_frame['head_spin_angle_cummulative'][0, sp][0,:] = head_spin_angle_cummulative
        
        if flag_automatic_head_spin_rotation:
            # Reading Lab Frame to Detect Spin Rotation        
            X_lab = variables_lab_frame['X'][0, sp]
            Y_lab = variables_lab_frame['Y'][0, sp]
            Z_lab = variables_lab_frame['Z'][0, sp]    
            
            is_trajectory_clockwise, trayectory_track_traslated = get_sperm_trayectory_direction(X_lab,Y_lab,Z_lab)
        else:
            # assuming that sperm spin counter_clock_wise. Read following paper
            # https://journals.biologists.com/jcs/article/136/22/jcs261306/335727
            is_trajectory_clockwise = False
        
        write_csv(Path(folder_root_vtk_output, sperm_id + ".csv"), head_spin_angle_cummulative)
        print(f"Sp_id={sperm_id}. Rotating clockwise: {is_trajectory_clockwise}\n-------")
        if (not is_trajectory_clockwise):
            head_spin_angle_cummulative = -head_spin_angle_cummulative
        
        for i in range(0,X_neck.shape[1]):
            tp = time_points[0,i]
            current_head_spin_angle_rad = np.deg2rad(head_spin_angle_cummulative[i])
            
            points = np.column_stack((X_neck[:,i], Y_neck[:,i], Z_neck[:,i]))
            
            swc_trace = points_to_swc(points) 
        
            
            # print(flagellum_direction)
            for ind in range(0,swc_trace.shape[0]):
                swc_trace[ind,2:5] = rodrigues_rotation(swc_trace[ind,2:5],np.array([1,0,0]),   -current_head_spin_angle_rad)
            
            X_neck[:,i], Y_neck[:,i], Z_neck[:,i] = swc_trace[:,2], swc_trace[:,3], swc_trace[:,4]
            
            
            swc_to_vtk_lines(Path(folder_vtk_output, f"sperm_{sperm_id}_HeadFixedFrame{tp:04}.vtk"), swc_trace)               
        variables_neck_frame['X'][0, sp] = X_neck
        variables_neck_frame['Y'][0, sp] = Y_neck
        variables_neck_frame['Z'][0, sp] = Z_neck
    
    variables_output = {"head_spin_angle": variables_neck_frame["head_spin_angle"],
                        "head_spin_angle_cummulative": 0,
                        "sperm_id": variables_neck_frame["sperm_id"],
                        "sperm_tp_analized": variables_neck_frame["sperm_tp_analized"],
                        "X": variables_neck_frame["X"],
                        "Y": variables_neck_frame["Y"],
                        "Z": variables_neck_frame["Z"],
        }
    sio.savemat(Path(folder_root,  file_head_frame_output_name), variables_output)
    
def get_sperm_trayectory_direction(X,Y,Z):
    flagellum_dir_track = np.empty((0,3))
    trayectory_track = np.empty((0,3))
    for i in range(X.shape[1]):
        
        points = np.column_stack((X[:, i], Y[:, i], Z[:, i]))
        swc_trace = points_to_swc(points) 
        
        #approximate flagellum direction
        current_direction = swc_trace[0,2:5]-get_point_reference(swc_trace[:,2:5], 5)
        current_direction = current_direction/np.linalg.norm(current_direction)
        
        flagellum_dir_track = np.vstack((flagellum_dir_track,current_direction))        
        trayectory_track = np.vstack((trayectory_track, get_point_reference(swc_trace[:,2:5], 35) ))
    
    mean_flagellum_dir = np.mean(flagellum_dir_track,axis=0)
    normal_vector_normalized = mean_flagellum_dir/np.linalg.norm(mean_flagellum_dir)
    
    trayectory_track_traslated = trayectory_track-np.mean(trayectory_track,axis=0)
    
    #projecting the vector in the plane with point at the origin at normal vector defined by mean_flagellum_direction
    #https://www.maplesoft.com/support/help/Maple/view.aspx?path=MathApps%2FProjectionOfVectorOntoPlane
    for i in range(0,trayectory_track_traslated.shape[0]):
        magnitud_ = np.dot(trayectory_track_traslated[i,:], normal_vector_normalized)
        trayectory_track_traslated[i,:] = trayectory_track_traslated[i,:] - magnitud_*normal_vector_normalized
    
    n_direction_clockwise=0
    n_total_points = 0
    
    #computing for each point if it is clockwise direction
    for i in range(2,trayectory_track_traslated.shape[0]):
        vec1 = trayectory_track_traslated[i-2,:] - trayectory_track_traslated[i-1,:] 
        vec2 = trayectory_track_traslated[i,:] - trayectory_track_traslated[i-1,:]
        
        val_dir = np.dot(np.cross(vec1,vec2),normal_vector_normalized)
        
        if val_dir>0:
            n_direction_clockwise+=1
            
        n_total_points+=1
        
    clockwise = False
    
    clockwise_measure = n_direction_clockwise/n_total_points
    print(clockwise_measure)
    if clockwise_measure>0.5:
        clockwise = True
    return clockwise, np.vstack((normal_vector_normalized,trayectory_track_traslated))
        
    
        
def get_point_reference(points, distance_ref):
    
    dist_ = np.sqrt(np.sum(np.power(np.diff(points, axis=0),2),axis=1))
    cumulative_dist = np.cumsum(dist_)
    ind = np.argmax(cumulative_dist>distance_ref)
    
    return (points[ind,:])

def convert_head_spin_from_range_0_90_to_full_rotations_0_360(head_spin_0_90):
    ind_0 = np.where(head_spin_0_90 == 0)[0]
    ind_90 = np.where(head_spin_0_90 == 90)[0]
    ind_0 = ind_0[0] if np.array(ind_0).size > 0 else np.inf
    ind_90 = ind_90[0] if np.array(ind_90).size > 0 else np.inf
    
    if ind_90 < ind_0:
        t_orientation = head_spin_0_90[:ind_90]
        t_orientation[t_orientation < 0] = np.finfo(float).eps
        head_spin_0_90[:ind_90] = t_orientation
        
        cummulative_orientation = np.cumsum(np.abs(np.diff(np.concatenate(([0], head_spin_0_90)))))
        
    else:
        # decreasing values scenario
        t_orientation = head_spin_0_90[:ind_0]
        t_orientation[t_orientation > 90] = 90 - np.finfo(float).eps
        head_spin_0_90[:ind_0] = t_orientation

        cummulative_orientation = np.cumsum(np.abs(np.diff(np.concatenate(([90], head_spin_0_90))))) + 90
        
    return cummulative_orientation
    
    
if __name__ == "__main__":
   main(sys.argv[1:])
   

# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:34:39 2021

@author: paul
"""
import scipy.io as sio
import numpy as np
import Python_Scripts.util.data as data_module
import Python_Scripts.util.util_vtk as util_vtk
from pathlib import Path
from os import mkdir
import sys


def main(argv):
    flagellum_dist_micras = 5
    
    
    #FILES NECK FRAME REFERENCE
    
    #SMOOTH SPLINES
    #file_labFrame = r'C:\Users\jalip\Documents\Proyectos\Sperm\Capacitados\Mat_File\Smooth_spline_p_0_0001/Capacitados_01_LabFrameReference_smoothSpline_p_0_0001.mat'
    
    #file_name_mat = 'Capacitados_02_NeckFrameReference_smoothSpline_p_0_0001'
    #file_neck_frame = r'C:\Users\jalip\Documents\Proyectos\Sperm\Capacitados\Mat_File\Smooth_spline_p_0_0001\\' + file_name_mat + '.mat'
    #folder_output = r'C:\Users\jalip\Documents\Proyectos\Sperm\Capacitados\Mat_File\Smooth_spline_p_0_0001\Head_Fixed_Frame_Method_Rotations_Traces_SmoothSpline_p_0_0001_' +  str(flagellum_dist_micras) + '_Microns_Rot_HeadSize'    


    
    file_labFrame = r'C:\Users\jalip\Documents\Proyectos\Sperm\Capacitados\Mat_File/Capacitados_01_LabFrameReference_raw.mat'

    file_name_mat = 'Capacitados_02_NeckFrameReference_raw'
    file_neck_frame = r'C:\Users\jalip\Documents\Proyectos\Sperm\Capacitados\Mat_File\\' + file_name_mat + '.mat'
    folder_output = r'C:\Users\jalip\Documents\Proyectos\Sperm\Capacitados\Mat_File\Head_Fixed_Frame_Method_Rotations_Traces_raw_' +  str(flagellum_dist_micras) + '_Microns_Difraction_head_spin'    
    
    #SPHERE ATTACHED_FLAGELLUM5
    #file_labFrame = r'C:\Users\jalip\Documents\Proyectos\Sperm\campo_claro_traces\Sphere_attached_to_flagellum\Sp_B001___trace_head_removed/Sphere_Attached_01_LabFrameReference_raw.mat'
    
    #file_name_mat = 'Sphere_Attached_02_NeckFrameReference_raw'
    #file_neck_frame = r'C:\Users\jalip\Documents\Proyectos\Sperm\campo_claro_traces\Sphere_attached_to_flagellum\Sp_B001___trace_head_removed\\' + file_name_mat + '.mat'
    #folder_output = r'C:\Users\jalip\Documents\Proyectos\Sperm\campo_claro_traces\Sphere_attached_to_flagellum\Sp_B001___trace_head_removed\Head_Fixed_Frame_Method_Rotations_Traces_SmoothSpline_p_0_0001_' +  str(flagellum_dist_micras) + '_Microns_Rot_HeadSize'       
    
    
    #Corrected microscope inversion
    file_labFrame = r'C:\Users\jalip\Documents\Proyectos\Sperm\Hermes_datos\Data\FIXED_AXIS\Lab_Frame_traces_ScienceAdvance_raw.mat'
    file_name_mat = 'neck_frame_traces_ScienceAdvance_raw_data_coordinates'
    file_neck_frame = r'C:\Users\jalip\Documents\Proyectos\Sperm\Hermes_datos\Data\FIXED_AXIS\\' + file_name_mat + '.mat'
    folder_output = r'C:\Users\jalip\Documents\Proyectos\Sperm\Hermes_datos\Data\FIXED_AXIS\Head_Fixed_Frame_Method_Rotations_Traces_raw_' +  str(flagellum_dist_micras) + '_Microns_Difraction_head_spin'    
    
    
    #loading data from mat file
    variables_neck_frame = sio.loadmat(file_neck_frame)
    variables_lab_frame = sio.loadmat(file_labFrame)
    
    if not(Path(folder_output).exists()):
        mkdir(folder_output)
    
    for sp in range(0,variables_neck_frame['X'].shape[1]):
        sperm_id = variables_neck_frame['sperm_id'][0,sp][0]
        
        file_output_data = Path(folder_output) / sperm_id
        if not(file_output_data.exists()):
            mkdir(file_output_data)
                
        #traces in Neck Fixed Frame for sperm sp using smoothing splines smoothing    
        X = variables_neck_frame['X'][0, sp]
        Y = variables_neck_frame['Y'][0, sp]
        Z = variables_neck_frame['Z'][0, sp]
        
        X_lab = variables_lab_frame['X'][0, sp]
        Y_lab = variables_lab_frame['Y'][0, sp]
        Z_lab = variables_lab_frame['Z'][0, sp]        
        
        time_points = variables_neck_frame['sperm_timePointsAnalyzed'][0,sp]
        head_spin_angle = variables_neck_frame['head_spin_angle'][0, sp][:,1]
                
        is_trajectory_clockwise = get_sperm_trayectory_direction(X_lab,Y_lab,Z_lab)
        
        #is_trajectory_clockwise = True
        
        print('Index {} Sperm_id  {} is rotating clockwise: {}'.format(sp, sperm_id,is_trajectory_clockwise))
        if (not is_trajectory_clockwise):
            head_spin_angle = -head_spin_angle
        
        for i in range(0,X.shape[1]):
            tp = time_points[i]
            current_head_spin_angle_rad = np.deg2rad(head_spin_angle[i])
            
            #swc trace from Hermes
            x = X[:,i].reshape((-1, 1))
            y = Y[:,i].reshape((-1, 1))
            z = Z[:,i].reshape((-1, 1))
            ids = np.arange(1, len(x)+1, 1).transpose().reshape((-1, 1))
            parents = ids-1
            parents[0] = -1
            
            swc_trace = np.hstack((ids, 0*ids, x, y, z, 0*ids, parents))  
        
            
            # print(flagellum_direction)
            for ind in range(0,swc_trace.shape[0]):
                swc_trace[ind,2:5] = data_module.rodrigues_rotation(swc_trace[ind,2:5],np.array([1,0,0]),   -current_head_spin_angle_rad)
            
            X[:,i] = swc_trace[:,2]
            Y[:,i] = swc_trace[:,3]
            Z[:,i] = swc_trace[:,4]
            
            
            util_vtk.swc_to_vtk_lines(file_output_data, sperm_id +'_'+data_module.tp2id(tp)+'.swc', swc_trace)               
        variables_neck_frame['X'][0, sp] = X
        variables_neck_frame['Y'][0, sp] = Y
        variables_neck_frame['Z'][0, sp] = Z
        
    #my_dict = {"X": data['X'], "Y": data['Y'], "Z":data['Z']}
    sio.savemat(Path(folder_output,  "03_Head_Fixed_Frame_Method_Rotations_Traces_raw_5_Microns_Difraction_head_spin.mat"), variables_neck_frame)
    
def get_sperm_trayectory_direction(X,Y,Z):
    flagellum_dir_track = np.empty((0,3))
    trayectory_track = np.empty((0,3))
    for i in range(0,X.shape[1]):
        
        x = X[:,i].reshape((-1, 1))
        y = Y[:,i].reshape((-1, 1))
        z = Z[:,i].reshape((-1, 1))
        ids = np.arange(0, len(x), 1).transpose().reshape((-1, 1))
        parents = ids-1
        parents[0] = -1
        
        swc_trace = np.hstack((ids, 0*ids, x, y, z, 0*ids, ids-1))
        
        #approximate flagellum direction
        current_direction = swc_trace[0,2:5]-get_point_reference(swc_trace[:,2:5], 10)
        current_direction = current_direction/np.linalg.norm(current_direction)
        
        flagellum_dir_track = np.vstack((flagellum_dir_track,current_direction))        
        trayectory_track = np.vstack((trayectory_track, get_point_reference(swc_trace[:,2:5], 15) ))
    
    mean_flagellum_dir = np.mean(flagellum_dir_track,axis=0)    
    normal_vector_normalized = mean_flagellum_dir/np.linalg.norm(mean_flagellum_dir)
    
    trayectory_track_traslated = trayectory_track-np.mean(trayectory_track,axis=0)
    
    #projecting the vector in the plane with point at the origin at normal vector defined by mean_flagellum_direction
    #https://www.maplesoft.com/support/help/Maple/view.aspx?path=MathApps%2FProjectionOfVectorOntoPlane
    for i in range(0,trayectory_track_traslated.shape[0]):
        magnitud_ = np.dot(trayectory_track_traslated[i,:],normal_vector_normalized)
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
    
    print((n_direction_clockwise/n_total_points))
    
    if (n_direction_clockwise/n_total_points)>0.5:
        clockwise = True
    return (clockwise)
        
    
        
def get_point_reference(points, distance_ref):
    
    dist_ = np.sqrt(np.sum(np.power(np.diff(points, axis=0),2),axis=1))
    cumulative_dist = np.cumsum(dist_)
    ind = np.argmax(cumulative_dist>distance_ref)
    
    return (points[ind,:])
    
if __name__ == "__main__":
   main(sys.argv[1:])
   

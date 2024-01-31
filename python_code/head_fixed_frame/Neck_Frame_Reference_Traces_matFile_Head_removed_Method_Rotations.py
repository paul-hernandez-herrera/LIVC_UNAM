# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 20:15:12 2021

@author: paul
"""
import os, sys
import scipy.io as sio
import numpy as np
from pathlib import Path
from util.basic_func import create_folder_in_case_not_exist, points_get_PCA_components, rodrigues_rotation
from util.util_swc import points_to_swc, swc_extract_trace_until_distance
from util.util_vtk import swc_to_vtk_lines

# set current folder as the working directory
workbook_dir = os.path.dirname(Path(__file__).parent.resolve())
os.chdir(workbook_dir)


def main(argv):
    # reading the data from input mat file with the following format
    # X, Y, Z cell with size n (every entry represents a sperm), columns represent the X, Y, Z coordinates at each time point while it has 100 points per time point
    # sperm_orientation cell with size n (every entry represents a sperm), first column represents the head sperm orientation in range [0, 90] while second column correspond to the cummulative rotation
    # sperm_timePointsAnalyzed cell with size n (every entry represents a sperm), contain information of the time points analyzed
    # sperm_id cell with size n (every entry represents a sperm), to identify the date that the sperm was adquired and experiment id
    
    flagellum_dist_micras = 5
    
    
    # here we read all the dataset information
    folder_path = r"C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\HIGH_VISCOCITY\data_traces"
    file_lab_input_name = "01_Lab_Frame_High_Viscocity_raw_fixed_n_points.mat"
    file_neck_output_name = "02_Neck_Frame_High_Viscocity_raw_fixed_n_points.mat"    
    
    folder_root_vtk_output = Path(folder_path, "02_Neck_Frame")
    create_folder_in_case_not_exist(folder_root_vtk_output)            
    
    #input data from mat file
    variables = sio.loadmat(Path(folder_path, file_lab_input_name))
    
    for sp in range(0,variables['X'].shape[1]):        
        sperm_id = variables['sperm_id'][0,sp][0]
        print(f"Running Sperm_id  {sperm_id}")
        folder_vtk_output = Path(folder_root_vtk_output, sperm_id)
        create_folder_in_case_not_exist(folder_vtk_output)
        
        time_points = variables['sperm_tp_analized'][0,sp]
        
        for i in range(0,variables['X'][0, sp].shape[1]):
            
            tp = time_points[i]
            
            points = np.column_stack((variables['X'][0, sp][:, i], variables['Y'][0, sp][:, i], variables['Z'][0, sp][:, i]))
            
            swc_trace = points_to_swc(points) 
            
            R, azimuth, elevation,flagellum_direction, swc_trace_translated = get_flagellum_direction_SphericaCoordinates(swc_trace,flagellum_dist_micras)
            
            # print(flagellum_direction)
            for ind in range(0,swc_trace.shape[0]):
                swc_trace_translated[ind,2:5] = rodrigues_rotation(swc_trace_translated[ind,2:5],np.array([0,0,1]), -azimuth)
                swc_trace_translated[ind,2:5] = rodrigues_rotation(swc_trace_translated[ind,2:5],np.array([0,1,0]), elevation)
            
            variables['X'][0, sp][:, i] = swc_trace_translated[:, 2]
            variables['Y'][0, sp][:, i] = swc_trace_translated[:, 3]
            variables['Z'][0, sp][:, i] = swc_trace_translated[:, 4]
            
            
            swc_to_vtk_lines(Path(folder_vtk_output, f"sperm_{sperm_id}_Raw_{tp:04}.vtk"), swc_trace)
            swc_to_vtk_lines(Path(folder_vtk_output, f"sperm_{sperm_id}_NeckFrame{tp:04}.vtk"), swc_trace_translated)

    variables_output = {"head_spin_angle": variables["head_spin_angle"],
                        "sperm_id": variables["sperm_id"],
                        "sperm_tp_analized": variables["sperm_tp_analized"],
                        "X": variables["X"],
                        "Y": variables["Y"],
                        "Z": variables["Z"],
        }      
    sio.savemat(Path(folder_path, file_neck_output_name), variables_output)
    
def get_sperm_trayectory_direction(time_points,X,Y,Z):
    flagellum_dir_track = np.empty((0,3))
    trayectory_track = np.empty((0,3))
    for i in range(0,len(time_points)):
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
        trayectory_track = np.vstack((trayectory_track, get_point_reference(swc_trace[:,2:5], 8) ))
    
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
    
    if (n_direction_clockwise/n_total_points)>0.5:
        clockwise = True
    return (clockwise)
        
    
def get_flagellum_direction_SphericaCoordinates(swc_head_removed, X_Micras):  
    # https://www.mathworks.com/help/phased/ug/spherical-coordinates.html
    #swc_head_removed: file containing the information of the trace with the head centerline points removed
    #X_Micras: center-line length from neckpoint to be used to compute flagellum direction
       
    # Translate trace to the origin
    swc_head_removed[:, 2:5] = swc_head_removed[:, 2:5] - swc_head_removed[0, 2:5]
    
    swc_flagellum = swc_extract_trace_until_distance(swc_head_removed,X_Micras)
    pca_flagellum = points_get_PCA_components(swc_flagellum[:,2:5])
    
    # direction from neck point to last_points flagellum
    dir_aprox = swc_flagellum[-1,2:5]-swc_flagellum[0,2:5]
    
    # get the first Principal Component
    flagellum_dir_pca = pca_flagellum[0,:]
    
    # Make sure that the eigenvector points from the first to the last point
    angle_vectors_rad = np.arccos(np.dot(dir_aprox,flagellum_dir_pca)/(np.linalg.norm(dir_aprox)*np.linalg.norm(flagellum_dir_pca)))
    
    if np.absolute(angle_vectors_rad)>(45*np.pi/180):
        # Eigenvector in the direction contrary to the flagellum orientation
        flagellum_dir_pca = -flagellum_dir_pca
        
    R = np.linalg.norm(flagellum_dir_pca)
    az = np.arctan2(flagellum_dir_pca[1],flagellum_dir_pca[0])
    el = np.arctan(flagellum_dir_pca[2]/np.linalg.norm(flagellum_dir_pca[0:2]))
    
    x_transf = R*np.cos(el)*np.cos(az)
    y_transf = R*np.cos(el)*np.sin(az)
    z_transf = R*np.sin(el)
    
    if np.any(np.abs([x_transf, y_transf, z_transf] - flagellum_dir_pca) > 0.01):
        raise NameError('Error at computing spherical coordinates')

    return R, az, el, flagellum_dir_pca, swc_head_removed
        
def get_point_reference(points, distance_ref):
    
    dist_ = np.sqrt(np.sum(np.power(np.diff(points, axis=0),2),axis=1))
    cumulative_dist = np.cumsum(dist_)
    ind = np.argmax(cumulative_dist>distance_ref)
    
    return (points[ind,:])
    
if __name__ == "__main__":
   main(sys.argv[1:])
   

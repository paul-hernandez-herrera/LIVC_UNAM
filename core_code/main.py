from .util import util
import numpy as np
import re,  pickle
from scipy.signal import find_peaks
from scipy import stats 
from pathlib import Path


def sort_file_names(input_path):
    # Automatically sort the file names in the folder based on a number in each file name, 
    # ensuring that each consecutive image has a consecutive number
    img_file_paths = util.get_image_file_paths(input_path)
    
    list_names = [[int(s) for s in re.findall(r'\d+', p.stem)] for p in img_file_paths]
        
    for i in range(0,len(list_names[0])):
        sorted_list = sorted(enumerate(list_names), key=lambda x: x[1][i])
        if all(np.diff([x[1][i] for x in sorted_list]) == 1):
            return [img_file_paths[x[0]] for x in sorted_list]
    return []
    
def create_stack_time_series_from_piezoelectric_info(input_path, input_txt, folder_output):
    
    input_path = sort_file_names(input_path)
    
    name_base = Path(folder_output).name
    
    z_val = 40*np.loadtxt(input_txt)  
    z_val = z_val[:len(input_path)]
    local_minimum, _ = find_peaks(-z_val)
    z_val[0:local_minimum[0]] = z_val[local_minimum[0]]
    
    local_maximum, _ = find_peaks(z_val)
    
    loc = np.sort(np.concatenate((local_minimum, local_maximum)))
    
    z_stack_size = stats.mode(np.diff(loc),keepdims=False)[0]
    
    info = {}
    tp = 0
    for stack_tp in range(0, len(local_minimum)-2):
        local_min_pos = loc[2*stack_tp]
        local_max_pos = loc[2*stack_tp+1]
        
        #this if is necesary to avoid local minimum due to vibrations of the piezo-electric device
        if (local_max_pos - local_min_pos)>5:
            img = []
            max_index = local_min_pos+z_stack_size
            
            for i in range(local_min_pos, max_index):
                img.append(util.imread(input_path[i]))
            img = np.stack(img)
            
            depth_z_val = z_val[local_min_pos:max_index]
            
            current_name = f"{name_base}_{tp:05d}"
            
            info[tp]  = {
                "lowerBoundZ": local_min_pos,
                "higherBoundZ": max_index,
                "zVal": depth_z_val,
                "current_name": current_name,
            }
            
            util.imwrite(Path(folder_output, f"{current_name}.tif"), img)
            np.savetxt(Path(folder_output, f"{current_name}.txt"), depth_z_val)
            tp+=1
            
    with open(Path(folder_output, f"{name_base}_info.pkl"), 'wb') as f:
        pickle.dump(info, f)            
            
            
    
from util.util import get_image_file_paths
import numpy as np
import re

def sort_file_names(input_path):
    # Automatically sort the file names in the folder based on a number in each file name, 
    # ensuring that each consecutive image has a consecutive number
    img_file_paths = get_image_file_paths(input_path)
    
    list_names = [[int(s) for s in re.findall(r'\d+', p.stem)] for p in img_file_paths]
        
    for i in range(0,len(list_names[0])):
        sorted_list = sorted(enumerate(list_names), key=lambda x: x[1][i])
        if all(np.diff([x[1][i] for x in sorted_list]) == 1):
            return [img_file_paths[x[0]] for x in sorted_list]
    return []
    

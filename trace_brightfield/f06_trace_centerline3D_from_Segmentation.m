function f06_trace_centerline3D_from_Segmentation()
    
    %parameters
    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp9_stacks';
    file_prefix =  'Exp9_stacks';
    seed_point_head = [383 275 11];
    stacks_index_to_trace = 1:273; 

    %parameters
    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp9_stacks';
    file_prefix =  'Exp9_stacks';
    seed_point_head = [383 275 11];
    stacks_index_to_trace = 1:273;     

    %running the trace for each time point
    for time_point = stacks_index_to_trace   
        clc;
        [~, seed_point_head]= extract_trace_from_segmentation(folder_path, file_prefix, time_point, seed_point_head);
    end
    
    f08_display_traces_xy_xz_yz(folder_path, file_prefix, stacks_index_to_trace) 
end
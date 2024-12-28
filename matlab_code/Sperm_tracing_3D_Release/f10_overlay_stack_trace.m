function f10_overlay_stack_trace(folder_path, stack_name_prefix, stacks_index_to_trace)

%parameters
folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp9_stacks\stacks_constant_sampling';
stack_name_prefix = 'Exp9_stacks';
stacks_index_to_trace = 1:274;

for stackID= stacks_index_to_trace
    close all;
    ID = get_TPID(stackID);
    
    
    current_file = [stack_name_prefix '_' ID '_DC'];
    current_name_SWC = [current_file '_trace.swc'];
    
    if exist(fullfile(folder_path,current_name_SWC),'file')         
        V = readStack(folder_path,current_file);
        SWC = readSWC(fullfile(folder_path,current_name_SWC));
        
        ind = sub2ind(size(V),SWC(:,3),SWC(:,4),SWC(:,5));
        V(ind) = 255;
        WriteRAWandMHD(V, [current_file '_overlay_stack'],folder_path)
      
    end
end
end
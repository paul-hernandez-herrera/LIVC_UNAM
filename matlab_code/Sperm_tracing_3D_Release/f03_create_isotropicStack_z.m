function f03_create_isotropicStack_z()
    %function to create isotropic stack in the z-axis
    %folder_path -> The path to the folder containing the stacks
    %stack_name_prefix -> prefix used for the stack's name
    folder_path =   'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks';
    stack_name_prefix = 'Exp2_stacks';   
    
    
    
    %FIXED PARAMETERS
    z_max = 20; %max height scaned by microscopy, for sperm it is usually fixed to 20 microns
    z_spacing = 0.5; %new spacing (Z voxel size in microns) in z-axis
    xy_spacing = 118/640; %spacing (x,y voxel size in microns) in x, y axis obtained by Dr. Corkidi
    folder_output = fullfile(folder_path, 'stacks_constant_sampling');
    
    %getting the fixed minimum height
    min_height  = get_minimum_Z_value_from_microscopy(folder_path,stack_name_prefix);
    new_sampling_Z = min_height:z_spacing:min_height+z_max;
    
    if not(exist(folder_output,'dir'))
        mkdir(folder_output);
    end
    
    
    for tp=1:999
        ID = get_TPID(tp);

        current_name = [stack_name_prefix  '_' ID]; 
        
        if exist(fullfile(folder_path,[current_name '_DC.mhd']),'file')
            stack = readStack(folder_path, [current_name '_DC']);
            heights = load(fullfile(folder_path, [current_name '.txt']));
            
            %sort heights to allow interpolation
            heights = alturas_in_ascending_order(heights); 
            
            %original mesh grid
            [X,Y,Z] = meshgrid((1:size(stack,2))*xy_spacing,(1:size(stack,1))*xy_spacing, heights);
            
            %new_mesh grid
            [X_new,Y_new,Z_new] = meshgrid((1:size(stack,2))*xy_spacing,(1:size(stack,1))*xy_spacing, new_sampling_Z);
            
            %obtaining the interpolated stack
            stack_interpolated = interp3(X,Y,Z,double(stack), X_new, Y_new, Z_new);
            
            %writing the new data
            WriteRAWandMHD(uint8(stack_interpolated), [current_name '_DC'],folder_output);
            csvwrite(fullfile(folder_output,[current_name '_DC.txt']), new_sampling_Z');          
        end

    end
    
    
end

function min_height  = get_minimum_Z_value_from_microscopy(folder_path,stack_name_prefix)
    %get the minimum value to be used for the stack

    min_height = [];
    for tp=1:999
        ID = get_TPID(tp);

        current_name = [stack_name_prefix  '_' ID];   
        
        txt_file_path =  fullfile(folder_path, [current_name '.txt']);
        if exist(txt_file_path,'file')
            heights = load(txt_file_path);            
            min_height = [min_height heights(1)];
        end

    end

    %assumming gaussian distribution to get the minimum value
    min_height = mean(min_height) - 3*std(min_height);

end

function alturas = alturas_in_ascending_order(alturas)
    for (i=1:length(alturas)-1)
        if (alturas(i)>=alturas(i+1))
            alturas(i+1)= alturas(i)+0.00001;
        end
    end
end
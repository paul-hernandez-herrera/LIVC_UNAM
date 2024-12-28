function f06_trace_centerline3D_brigthfield()
    
    %parameters
    % Nota DE IAN: Aqui pones la ruta de la base de datos y el nombre del
    % conjunto de datos
    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks\stacks_constant_sampling';
    stack_name_prefix =  'Exp2_stacks';
    % NOTA DE IAN: Aqui pones el nombre del archivo que te genero el otro
    % codigo
    file_name_endpoints = 'Exp2_stacks_endPoints_2.mat';
    threshold_head = 110;
    seed_point_head = [538 291  22]; 
    stacks_index_to_trace = [1 : 274]; 
    
%     folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\Exp3_stacks_DC\stacks_constant_sampling';
%     stack_name_prefix =  'Exp3_stacks';
%     % NOTA DE IAN: Aqui pones el nombre del archivo que te genero el otro
%     % codigo
%     file_name_endpoints = 'Exp3_stacks_endPoints_1.mat';
%     threshold_head = 110;
%     seed_point_head = [360 217  24]; 
%     stacks_index_to_trace = [1 : 274];
%     stacks_index_to_trace = [1 : 5];

    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp8_stacks\stacks_constant_sampling';
    stack_name_prefix =  'Exp8_stacks';
    % NOTA DE IAN: Aqui pones el nombre del archivo que te genero el otro
    % codigo
    file_name_endpoints = 'Exp8_stacks_endPoints_1.mat';
    threshold_head = 120;
    seed_point_head = [385 274  24]; 
    stacks_index_to_trace = [1 : 100];  
    seed_point_head = [382 272 22]; 
    stacks_index_to_trace = [101 : 274];  

    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp9_stacks\stacks_constant_sampling';
    stack_name_prefix =  'Exp9_stacks';
    % NOTA DE IAN: Aqui pones el nombre del archivo que te genero el otro
    % codigo
    file_name_endpoints = 'Exp9_stacks_endPoints_1.mat';
    threshold_head = 120;
    seed_point_head = [385 274  24]; 
    stacks_index_to_trace = [1 : 273];    

    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp11_stacks\stacks_constant_sampling';
    stack_name_prefix =  'Exp11_stacks';
    % codigo
    file_name_endpoints = 'Exp11_stacks_endPoints_1.mat';
    threshold_head = 120;
    seed_point_head = [308 323 8]; 
    stacks_index_to_trace = [1 : 273]; 

    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp12_stacks\stacks_constant_sampling';
    stack_name_prefix =  'Exp12_stacks';
    % codigo
    file_name_endpoints = 'Exp12_stacks_endPoints_1.mat';
    threshold_head = 130;
    seed_point_head = [401 323 11]; 
    stacks_index_to_trace = [1 : 273];  

    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp13_stacks\stacks_constant_sampling';
    stack_name_prefix =  'Exp13_stacks';
    % codigo
    file_name_endpoints = 'Exp13_stacks_endPoints_1.mat';
    threshold_head = 135;
    seed_point_head = [412 322 8]; 
    stacks_index_to_trace = [1 : 180];      
    
    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp16_stacks\stacks_constant_sampling';
    stack_name_prefix =  'Exp16_stacks';
    % codigo
    file_name_endpoints = 'Exp16_stacks_endPoints_1.mat';
    threshold_head = 125;
    seed_point_head = [320 248 15]; 
    stacks_index_to_trace = [1 : 273]; %SeedZ+6
    
    seed_point_head = [308 251 9 ]; 
    stacks_index_to_trace = [218 : 273]; %SeedZ+6

    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp17_stacks\stacks_constant_sampling';
    stack_name_prefix =  'Exp17_stacks';
    % codigo
    file_name_endpoints = 'Exp17_stacks_endPoints_1.mat';
    threshold_head = 125;
    seed_point_head = [395 327 18]; 
    stacks_index_to_trace = [221:273];    

    %running the trace for each time point
    for time_point = stacks_index_to_trace    
        clc;
        [~, seed_point_head]= rec_fragelo_CampoClaro_stopTerminalPoint_NOSEGMENTATION(folder_path, stack_name_prefix, time_point, file_name_endpoints, seed_point_head,threshold_head);
    end
    
    f08_display_traces_xy_xz_yz(folder_path, stack_name_prefix, stacks_index_to_trace) 
end
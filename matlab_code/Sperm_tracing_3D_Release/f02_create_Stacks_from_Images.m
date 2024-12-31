function f02_create_Stacks_from_Images()
    %folder_path -> The path to the folder containing the images
    %image_prefix -> sufix used to identify the images. Image file name should be [image_prefix + 8 id numbers + .tif]
    %folder_output -> The path to the folder where the stacks will be saved
    %stack_name_prefix -> prefix used to save the stacks
    %shift -> parameter used to make sure that the images match with the values of the txt heights

    %{
    Parametro fijo es el voltaje utilizado, este parametro es importante
    para obtener el valor correcto de alturas
    %}
    conversion = 10; % Fecha 2024_11
    % conversion = 40; % Fecha Antes de 2024_11
    

    folder_path =   'E:\SPERM\campo_claro\VERY_HIGH_VISCOCITY\171207 NAC Very High Viscosity 7 dic 2017\Exp 2\Exp 2';
    image_prefix = 'Exp 2_';
    folder_output = 'E:\SPERM\campo_claro\VERY_HIGH_VISCOCITY\171207 NAC Very High Viscosity 7 dic 2017\Exp 2\Exp2_stacks';
    stack_name_prefix = 'Exp2_stacks';
    shift = -1; 
    


    %solo guardatemos las subidas del microscopio
    HacerStacksSubida = true;
    
    %imagenes comienzan en indice 0 mientras que heighsts a indice 1. Sumar
    %valor 1 al shift
    shift = shift +1;

    nz = length(dir(fullfile(folder_path,'*.tif')));

    if (not(exist(folder_output,'dir')))
        mkdir(folder_output);
    end

    close all;
    voltage = dir(fullfile(folder_path,'*.txt'));

    Z_val = conversion*csvread(fullfile(folder_path,voltage(1).name));

    Z_val = Z_val(1:nz-shift);

    [~,loc1]=findpeaks(Z_val);
    [~,loc2]=findpeaks(-Z_val);
%     loc2(1:20)
    loc = sort([loc1;loc2]);
    loc = [1; loc; nz-shift+1];
    loc = unique(loc);
    loc = loc + shift-1;
    it=1;
    while (Z_val(it+1)-Z_val(it))==0
        it=it+1;
    end

    if (Z_val(it+1)-Z_val(it))>0
        %Primer stack es subida
        FLAG_SUBIDA = true;
    else
        FLAG_SUBIDA = false;
    end

    if (HacerStacksSubida)
        if (FLAG_SUBIDA)
            %subida inician en el primer stack
            loc1 = loc(1:2:end); loc2 = loc(2:2:end);
        else
            loc1 = loc(2:2:end); loc2 = loc(3:2:end);
        end
    else
        if (FLAG_SUBIDA)
            %bajada inician en el segundo stack
            loc1 = loc(2:2:end);loc2 = loc(3:2:end);
        else
            loc1 = loc(1:2:end);loc2 = loc(2:2:end);
        end
    end

    loc1 = loc1(3:end-1);
    loc2 = loc2(3:end-1);



    z_stackSize = mode(diff(loc)+1);

    % Current_stack = zeros(nx,ny,z_stackSize,'uint8');
    tp = 1;
    for i=1:length(loc1)-1

        lowB = loc1(i);
        highB = loc2(i);

        if ((highB-lowB) >  5)
            

            ID = get_TPID(tp);

            current_name = [stack_name_prefix  '_' ID];

            z_CurrentStack = highB-lowB+1;
            if (z_CurrentStack<z_stackSize)
                index_ = lowB:highB;
                for ii=z_CurrentStack+1:z_stackSize
                    index_ = [index_ highB];
                end
            elseif (z_CurrentStack>z_stackSize)
                index_ = lowB:lowB+z_stackSize-1;
            else
                index_ = lowB:highB;
            end
            %images begin at index 000000
            index_ = index_ -1;

            Current_stack = read_camImage(index_,folder_path, image_prefix);  
%             Current_stack(:,1:20,:)=0;
%             Current_stack(:,end-20:end,:)=0;

            %Just to have the minimum to start at zero
            current_min =  min(Current_stack(:));
        %     Current_stack = Current_stack - min(Current_stack(:));

            WriteRAWandMHD(Current_stack, current_name , folder_output,[1 1 1]);
            %write_tif(Current_stack,folder_output,current_name)

            %saving current stack information
            info{tp}.lowerBoundZ = lowB;
            info{tp}.higherBoundZ = highB;
        %     if (FLAG_SUBIDA)
            info{tp}.zVal = Z_val((index_+1) -shift +1);

            if (any(diff(info{tp}.zVal)<0))
                error('Z_val not decreasing values');
            end

            csvwrite(fullfile(folder_output,[current_name '.txt']),info{tp}.zVal);
        %     end
            info{tp}.current_name = current_name;
            info{tp}.minVal = current_min;
            
            tp = tp + 1;
        end

    end

    name_variable = fullfile(folder_output,strcat(stack_name_prefix,'_info.mat'));
    save(name_variable,'info');

    display_Projections_xy_xz_yz(folder_output,stack_name_prefix)
end

function stack = read_camImage(index_,folder_path,file_ID)
    for i=1:length(index_)
        ID = sprintf('%08d', index_(i));                      
    %     ID = num2str(index_(i)); 
        I = imread(fullfile(folder_path,[file_ID  ID '.tif']))';
        if i==1
            stack = zeros(size(I,1),size(I,2),length(index_),'uint8');
        end
    
        stack(:,:,i)= I;
    end
end
function f01_get_shift_values_forCreatingStacks()    
    %folder_path -> The path to the folder containing the images
    %image_prefix -> sufix used to identify the images. Image file name should be [image_prefix + 8 id numbers + .tif]
    %crop -> crop containing the sperm head in the firsts 1,000 images

    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\Exp2';
    image_prefix = 'Exp2_TP_';
    crop = [495 250 ;580 330 ];      

    TP_high = 1000;
    
    stack = [];  % Inicializar el stack
    
    for i = 0:TP_high
        % Generar ID con ceros iniciales
        ID = sprintf('%08d', i); 
        
        % Leer la imagen
        I = imread(fullfile(folder_path, [image_prefix ID '.tif']))';
        
        % Inicializar stack si está vacío
        if isempty(stack)
            stack = zeros(size(I, 1), size(I, 2), TP_high, 'uint8');
        end
        
        % Almacenar la imagen en el stack
        stack(:, :, i + 1) = I;
    end

    % Convertir stack a single y calcular intensidad media
    stack = single(stack);
    mean_intensityStack = mean(stack(:));
    
    % Recortar el stack
    stack = stack(crop(1,1):crop(2,1), crop(1,2):crop(2,2), :);
    
    % Mostrar la proyección máxima del stack
    imshow(max(stack(:, :, 1:TP_high), [], 3), []);
    
    % Inicializar intensidad
    intensity = zeros(TP_high - 50, 1);
    
    % Calcular intensidad logarítmica
    for i = 45:TP_high-50
        stack_a = stack(:, :, i-10:i);
        stack_b = stack(:, :, i+10:-1:i);
        diff_abs = abs(stack_a - stack_b);
        intensity(i) = log(sum(diff_abs(:)));
    end

    % Ajustar valores iniciales de intensidad y suavizar
    intensity(1:44) = max(intensity);
    s_int = smooth(intensity, 5);
    
    % Encontrar picos
    [~,loc_peak]=findpeaks(-s_int);
    loc_peak(1)=[];
    loc_peak(loc_peak>TP_high-55)=[];
    mean_int = mean(s_int);
    loc_peak = loc_peak(s_int(loc_peak)<mean_int);
    
    for i=1:length(loc_peak)
        c_ind = loc_peak(i);
        [~,pos]=min(intensity(c_ind-5:c_ind+5));
        loc_peak(i) = c_ind-5+pos-1;
    end
    
    % Mostrar resultados
    fprintf("Loc from Images\n");
    disp(loc_peak');
    
%     fprintf('\n\n peaks txt file\n');
    voltage = dir(fullfile(folder_path,'*.txt'));

    Z_val = 10*csvread(fullfile(folder_path,voltage(1).name));
    [~,loc1]=findpeaks(Z_val);
    %positions for bottom
    [~,loc2]=findpeaks(-Z_val);
    loc = loc2;
    
    loc(loc>TP_high-55) = [];
    loc(loc<loc_peak(1)) = [];
    fprintf("\n\nLoc from Z TXT\n")
    loc'
    
    list_shift = [];
    for i=2:length(loc)-1
        diff_peak = loc_peak - loc(i);
        [~,pos] = min(abs(diff_peak));
        min_val = diff_peak(pos);
        if abs(min_val) > 25
            min_val = [];
        end
        list_shift = [list_shift; min_val];
    end
    
    fprintf('\n\n')
    
    fprintf('shift value is: %g',round(mean(list_shift)));
    
    fprintf('\n\n')
    
end

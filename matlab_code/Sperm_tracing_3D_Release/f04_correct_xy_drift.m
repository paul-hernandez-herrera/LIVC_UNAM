function f04_correct_xy_drift()
    %path to fiji scripts
    %{
    MAKE SURE TO SET THE CORRECT PATH FOR THE FIJI scripts folder
    %}
    addpath('C:\Users\paulh\Documents\Software\Fiji.app\scripts'); 
    
    
    folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241210 CC 4000fps Calceina y Fluo 4000fps - 90hz 20 micras\STACKS\Exp7_stacks';
    stack_name_prefix = 'Exp7_stacks'; 
    threshold_head = 140;
    seed_point_head = [543 171 11];
    TP_initial = 1;
    
    zVal_ref = get_zVal_ref(folder_path, stack_name_prefix);

    mov_piezo = [];
    for tp=TP_initial:999    
        close all;

        ID = get_TPID(tp);

        file_name = [stack_name_prefix '_' ID];fprintf([file_name '\n'])

        if exist(fullfile(folder_path,[file_name '.mhd']),'file')
            %reading 3D image stack
            V = readStack(folder_path,file_name);
            alturas = load(fullfile(folder_path,[file_name '.txt']));

            seed_point_head = getHeadPosition(V>threshold_head,seed_point_head,threshold_head);

            x_head = seed_point_head(1);
            y_head = seed_point_head(2);

            window_size = 70;
            
            % Coordenadas ajustadas al tamaño del volumen
            x_min = max(1, x_head - window_size);
            y_min = max(1, y_head - window_size);
            x_max = min(size(V, 1), x_head + window_size);
            y_max = min(size(V, 2), y_head + window_size);
            
            % Fix not uniform illumination
            V_Cor_illum = single(V) - imclose(imopen(single(V),ones(10,10,1)),ones(20,20,1)); 

            h = fspecial('average', [5, 5]);
            for i =[1:size(V,3)]
                V_Cor_illum(:,:,i)=imfilter(V_Cor_illum(:,:,i), h);
            end

            %setting a new volume to keep the cropped volume. Center of the volume
            cropped_head = single(V_Cor_illum(x_min:x_max,y_min:y_max,:));

            mean_val = mean(cropped_head(:));
            cropped_head = abs(cropped_head-mean_val);
            cropped_head = normalizeVol(cropped_head,0,255);


            cropped_head_driftCorrected = uint8(stackRegWrapper(uint8(cropped_head), '[Translation]'));

            [TX, TY] = deal([]);
            for zz=1:size(cropped_head_driftCorrected,3)
                current_slice = cropped_head_driftCorrected(:,:,zz);
                tx = 0;
                for x=1:size(current_slice,1)
                    line = current_slice(x,:);
                    if sum(line)==0
                        if (x>size(current_slice,1)/2)
                            tx = x-size(current_slice,1) -1;
                            break;
                        else
                            tx = x;
                        end
                    end
                end

                ty = 0;
                for y=1:size(current_slice,2)
                    line = current_slice(:,y);
                    if (sum(line)==0)
                        if (y>size(current_slice,2)/2)
                            ty = y-size(current_slice,2) -1;
                            break;
                        else
                            ty = y;
                        end
                    end
                end


                TX = [TX;tx];
                TY = [TY;ty];

            end

            min_x = min(TX);
            min_y = min(TY);
            max_x = max(TX);
            max_y = max(TY);

%             V= cropped_head;
            TV = uint8([max_x-min_x+1+size(V,1), max_y-min_y+1+size(V,2), size(V,3)]);
            for zz=1:size(V,3)
                TV(TX(zz)-min_x+1:TX(zz)-min_x+size(V,1),TY(zz)-min_y+1:TY(zz)-min_y+size(V,2),zz) =V(:,:,zz);
            end

            %reference for traslation is the z value in the midle
            distance_ = pdist2(zVal_ref, alturas);

            [~,ref_z] = min(distance_);ref_z = ref_z(1);

%                         fprintf('Traslation = %g %g --- ref = %g\n',TX(ref_z)-TX(1),TY(ref_z)-TY(1),ref_z);
%                 ref_z = round(size(V,3)/2);
            mov_piezo =[mov_piezo; TX(ref_z)-TX(1) TY(ref_z)-TY(1)];
            
            Translation = [TX-TX(ref_z)+TX(1), TY-TY(ref_z)+TY(1)];
            csvwrite(fullfile(folder_path,[file_name '_drift_translation.txt']), Translation);

            TV = TV(TX(ref_z)-min_x+1:TX(ref_z)-min_x+size(V,1),TY(ref_z)-min_y+1:TY(ref_z)-min_y+size(V,2),:);

            WriteRAWandMHD(TV,[file_name '_DC'], folder_path); 
            %WriteRAWandMHD(cropped_head_driftCorrected,[file_name '_HS_DriftCorrected'],file_path{z}); 
        end
    end
    
%     figure;plot(mov_piezo(:,1),mov_piezo(:,2))
    
end

function zVal_ref = get_zVal_ref(folder_path, stack_name_prefix)

    for tp=1:999
        ID = get_TPID(tp);

        current_name = [stack_name_prefix  '_' ID]; 
        
        if exist(fullfile(folder_path,[current_name '.mhd']),'file')
            heights = load(fullfile(folder_path, [current_name '.txt']));
            zVal_ref = heights(floor(length(heights)/2));
            break;
        end
    end
end

function headPos = getHeadPosition(B,seed_point_head,threshold_head)
%     B(:,:,17:end)=0;
%just one head per stack
if threshold_head>=250
    B = imerode(B,ones(3,3,3));
end

X=[];
Y=[];
Z=[];
min_size = 30;
conComp = bwconncomp(B,26);
[~,~,nz] =size(B);
if (isempty(seed_point_head))
    min_size = -inf;
    for i=1:conComp.NumObjects
        current_size = size(conComp.PixelIdxList{i},1);
        if (current_size>min_size)

            [I,J,K] = ind2sub(size(B),conComp.PixelIdxList{i});
            X = round(mean(I));
            Y = round(mean(J));
            Z = round(mean(K));
            min_size = current_size;
            headPos = [X Y Z]';
        end
    end
else
    min_dist = inf;
    
    for i=1:conComp.NumObjects
        if not(exist('headPos','var'))
            
             [I,J,K] = ind2sub(size(B),conComp.PixelIdxList{i});
             X = round(mean(I));
             Y = round(mean(J));
             Z = round(mean(K));            
             headPos = [X Y Z]';
        end
        if length(conComp.PixelIdxList{i})>min_size
             [I,J,K] = ind2sub(size(B),conComp.PixelIdxList{i});
             X = round(mean(I));
             Y = round(mean(J));
             Z = round(mean(K));
             dist_ = sqrt((X-seed_point_head(1))^2 + (Y-seed_point_head(2))^2 +(Z-seed_point_head(3))^2);
%              dist_ = length(conComp.PixelIdxList{i});

%             if (dist_<min_dist )
            if (dist_<400 )                
%                 dist_ = length(conComp.PixelIdxList{i});
                if (dist_<min_dist )                
                    headPos = [X Y Z]';
                    min_dist = dist_;
                end
            end
        end
    end
    if min_dist == inf
        disp('Warning setting new head position as previous position')
        headPos = seed_point_head;
    end
end
end
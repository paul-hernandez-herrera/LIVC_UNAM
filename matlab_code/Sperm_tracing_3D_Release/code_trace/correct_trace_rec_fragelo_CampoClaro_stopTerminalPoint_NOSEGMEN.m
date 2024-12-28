function [file_name ,seed_point_head]= correct_trace_rec_fragelo_CampoClaro_stopTerminalPoint_NOSEGMEN(folder_path, stack_name_prefix, timePoint, file_endpoints, seed_point,thresholdHead, V_GUI, seed_point_GUI, stop_point_GUI, swc_GUI)
%close all;
folder_projection_output = fullfile(folder_path,'trace_projections_xy');
if not(exist(folder_projection_output,'dir'))
    mkdir(folder_projection_output);
end

%maximum number of voxels to trace in the second iteration
length_segment = 200;


show_image_in_screen = false;


ID = get_TPID(timePoint);
file_name = [stack_name_prefix '_' ID '_DC'];


fprintf(['\nProcessing \n' file_name]);

fast_marching_fileName = [file_name '_fM'];


%Reading the raw volume
%[V_raw,SPACING]=readStack(folder_path,file_name); V_raw=single(V_raw);
V_raw = V_GUI; V_raw = single(V_raw);

% V_raw = fill_microscope_holes(V_original, V_raw);

if all(seed_point_GUI>[0, 0, 0])
    %getting seed point from GUI 
    seed_point = seed_point_GUI';
else
    if not(isempty(swc_GUI))
        seed_point = swc_GUI(1,3:5)';
    else
        file_namePrev = [stack_name_prefix '_' get_TPID(timePoint-1) '_DC'];
        if  exist(fullfile(folder_path,[file_namePrev '_LogN_rec_FM.swc']),'file')
            %taking previous seed point as a prior knowledgue to detect current
            %seed point
            SWC =readSWC(fullfile(folder_path,[file_namePrev '_LogN_rec_FM.swc']));

            seed_point = SWC(1,3:5)';
        end

        %get sperm's head position
        seed_point = getHeadPosition(V_raw>thresholdHead,seed_point,thresholdHead);
    end
end
% seed_point = [300 126 16]';
seed_point_head = seed_point;

if exist(fullfile(folder_path,file_endpoints),'file')
    tracked_points = load(fullfile(folder_path,file_endpoints));
end


% Just in case that we need to redo tracing to without changing terminal
% point
% if  exist(fullfile(folder_path,[file_name '_rec_FM.swc']),'file')
%     SWC =readSWC(fullfile(folder_path,[file_name '_rec_FM.swc']));
%     stop_point2 = SWC(end,3:5)';
% else
%     stop_point2 = [];
% end



%Parameters FASTMARCHING
%number maximum of iteration for fast_marching
nb_iter_max = 50000000;

%neighborhood to extract head for smoothing
win_size=25;
x_min = seed_point(1)-win_size; if (x_min<1); x_min=1;end
x_max = seed_point(1)+win_size; if (x_max>size(V_raw,1)); x_max = size(V_raw,1); end
y_min = seed_point(2)-win_size; if (y_min<1); y_min=1;end
y_max = seed_point(2)+win_size; if (y_max>size(V_raw,2)); y_max = size(V_raw,2); end

%para homogeneizar las intensidades
V_raw = V_raw - imclose(imopen(V_raw,ones(10,10,1)),ones(10,10,1));

max_value_CF = 50;
V_raw( V_raw >max_value_CF ) =max_value_CF;


%dilate the cropped volume to avoid tracing problems near the head
V_rawClosed = imdilate(V_raw(x_min:x_max,y_min:y_max,:),ones(3,3,1));


CostFunction = V_raw;
CostFunction = imdilate(CostFunction,ones(3,3,3));
CostFunction(x_min:x_max,y_min:y_max,:) = max_value_CF*V_rawClosed/max(V_rawClosed(:));
CostFunction(CostFunction >max_value_CF) = max_value_CF;

% CostFunction(CostFunction<5)=5;
% CostFunction(109:114,365:376,18:20)=max_value_CF;

%gaussian smoothing
aspect_ratio = [1 1 0.5];
G = Gaussian3D(2*aspect_ratio, round([7*aspect_ratio(1), 7*aspect_ratio(2), 7*aspect_ratio(3)]));
CostFunction = convn(CostFunction,G,'same');


% CostFunction(:,:,1:6)=0;

CostFunction= CostFunction/max(CostFunction(:)); imageToDisplay = V_raw;



label_display_image = 'off';
if (show_image_in_screen)
    label_display_image = 'on'; 
end
h = figure;hAxes = gca;set(h,'Visible', label_display_image); imshow(max(imageToDisplay,[],3)',[],'Parent',hAxes);colormap('gray');hold on;
c = {'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b' 'g' 'b'  'g' 'b'  'g' 'b'  'g' 'b'  'g' 'b'  'g' 'b'  'g' 'b'  'g' 'b'};


several_seeds = false;

for step=1:1
    stop_points=[];

        
    if all(stop_point_GUI>[0, 0, 0])
        stop_points = stop_point_GUI';
    elseif not(isempty(swc_GUI))
        stop_points = swc_GUI(end,3:5)';
    elseif exist('tracked_points.z_SP','var')
        if tracked_points.z_SP{timePoint}>0
            stop_points = [tracked_points.x_SP{timePoint}; tracked_points.y_SP{timePoint}; tracked_points.z_SP{timePoint}];
        else
            for i=1:size(CostFunction,3)
                stop_points = [stop_points [tracked_points.x_SP{timePoint}; tracked_points.y_SP{timePoint};i]];
            end 
        end
    else
        for i=1:size(CostFunction,3)
            stop_points = [stop_points [tracked_points.x_SP{timePoint}; tracked_points.y_SP{timePoint};i]];
        end    
    end
    
     
%     if not(isempty(stop_point2))
%         stop_points = stop_point2;
%     end
%     stop_points = [493 330 13]';
     fprintf('\n');    
    
    if several_seeds 
%         stop_points = [165 188 8; 166 169 12;170 175 13;178 174 14 ;189 191 15]';
        stop_points = stop_points(:,step);
    end    
     
    %maximum length to detect
    if (step==1)
        current_length = 350;        
    else
        current_length = length_segment+5;
    end

    
    [m_c,M_c]=crop_volume(CostFunction,seed_point,current_length);
    
    %cropping the volume just to search in the region of interest
    CostFunction2 = CostFunction(m_c(1):M_c(1),m_c(2):M_c(2),m_c(3):M_c(3)); 
    CostFunction2(:) = normalizeVol(double(CostFunction2(:)), 0, 1);
    CostFunction2 = exp(40*CostFunction2);
    

    bMask = true(size(CostFunction2));
    seed_point = seed_point - m_c' + [1 1 1]'; 
    for i=1:3
        stop_points(i,:) = stop_points(i,:) - m_c(i)' + [1]'; 
    end
    I = false([1,size(stop_points,2)]);
    for i=1:3
        I = I | (stop_points(i,:)>size(CostFunction2,i) | stop_points(i,:)<1) ; 
    end
    
    stop_points(:,I)=[];
    
    if isempty(stop_points)
        stop_points = [1;1;1];
    end
    
    %running fast marching
    [fast_marching, S] = compute_fast_marching(bMask, CostFunction2, seed_point, stop_points, current_length,nb_iter_max, folder_path, fast_marching_fileName , true, [1 1 1]);
    clear bMask CostFunction2;
    ind = sub2ind(size(S),stop_points(1,:),stop_points(2,:),stop_points(3,:) );
    I = S>10000000;
    S(I)=0;
    val = S(ind);
    if any(val>0)
        [~,ind]=max(val);
        end_points = stop_points(:,ind);  
    else
        
        [~,index] = max(S(:));
        [x,y,z] = ind2sub(size(S),index);
        end_points = [x,y,z]';          
    end

    
    %extract centerline
    [a,~] = traceBack_centerline3D([],seed_point,end_points,fast_marching,[],folder_path,fast_marching_fileName); clear fast_marching S;
    
     if sum(val)==0
         %terminal point has not been reached
        a{1} = a{1}(1:end-5,:); 
     end
     for i=1:3
         a{1}(:,i)= a{1}(:,i) + m_c(i) -1;
     end
         

    index_ = sub2ind(size(CostFunction),a{1}(:,1),a{1}(:,2),a{1}(:,3));



    
    plot(a{1}(:,1),a{1}(:,2),c{step},'Parent',hAxes);
    %saving segments
    segments{step} = a{1};
    radius{step} = CostFunction(index_);
    max_r = max(radius{step});    
    max_r = 1;  
    if sum(val)>0
        if not(several_seeds)
            break;
        end
    end
    
%     fprintf('Max radius = %4.2f\n',max_r) ;
    if max_r <1
        max_r = 1;
    end
    %points to reduce speed  

% % %     if (step==1)
% % %         mask = get_mask(CostFunction,segments{step},2*aspect_ratio,2*max_r);
% % %     else
% % %         mask = get_mask(CostFunction,segments{step},2*aspect_ratio,2*max_r);
% % %     end
% % %     
% % %     CostFunction(mask) = 0;
% % % 
% % %     hold on;
% % %     seed_point = segments{step}(end,:)';
end
%plot(tracked_points.x_SP{timePoint},tracked_points.y_SP{timePoint},'m.','Parent',hAxes);
print(h,fullfile(folder_projection_output, [file_name '_rec.png']),'-dpng')
close(h);



%creating the SWC file
createSWCfromSegments(segments, radius, folder_path, [file_name '_trace.swc'], [1 1 1]);
SWCtoVTK(folder_path, [file_name '_trace.swc']);

delete_RAW(folder_path,fast_marching_fileName);

clear tracked_points Probability CostFunction;
end

function [m_c,M_c]=crop_volume(V,seed_point,current_length)

vol_size = size(V);

for i=1:3
    m_c(i) = seed_point(i)-current_length;
    M_c(i) = seed_point(i)+current_length;
    if (m_c(i)<1)
        m_c(i)=1;
    end
    if (M_c(i)>vol_size(i))
        M_c(i)=vol_size(i);
    end
end
    
end

function headPos = getHeadPosition(B,seed_point,thresholdHead)
% B(:,:,1:10)=0;
% B = imerode(B,ones(3,3,3));

%     B(:,:,1:5)=false;
%     B(:,:,25:end)=false;

if thresholdHead>=250
    B = imerode(B,ones(3,3,3));
end


% B = imerode(B,ones(3,3,5));
%just one head per stack
X=[];
Y=[];
Z=[];
min_size = 5;
% min_size = 5;
conComp = bwconncomp(B,26);
[~,~,nz] =size(B);
if (isempty(seed_point))
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
             dist_ = sqrt((X-seed_point(1))^2 + (Y-seed_point(2))^2 +(Z-seed_point(3))^2);
%              dist_ = length(conComp.PixelIdxList{i});

%             if (dist_<min_dist )
            if (dist_<40 )                
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
        headPos = seed_point;
    end
end

end

function mask = get_mask(fast_marching,segment,anisotropy,radius)
% segment(end-3:end,:)=[];
index = sub2ind(size(fast_marching),segment(:,1),segment(:,2),segment(:,3));

mask = false(size(fast_marching));

mask(index)=true;
%mask = bwdist(mask);
DT=bwdistsc1(mask,[anisotropy(1) anisotropy(2) 1/anisotropy(3)],radius);
mask = DT<radius;

% WriteRAWandMHD(DT,'exp10-crop1_TP051_DT','/home/paulhh/Projects/Sperms/ManualTrace_Z/integral-Fluo-080316-exp10-crop1/exp10-crop1/toReconstruct2');
% mask2 = false(size(fast_marching));
% mask2(index(end))=true;
% DT=bwdistsc1(mask2,[anisotropy(1) anisotropy(2) 1/anisotropy(3)],radius);
% mask2 = DT<radius;
I =find(mask);
[x,y,z] = ind2sub(size(mask),I);

% v1 = segment(end,:) - segment(end-2,:);
v1 = getDirectionFromPoints(segment(end-5:end,:));


val1 = v1(1).*(x-segment(end-2,1)) + v1(2).*(y-segment(end-2,2)) + v1(3).*(z-segment(end-2,3));
%val2 = v2(1).*(x-segment(1,1)) + v2(2).*(y-segment(1,2)) + v2(3).*(z-segment(1,3));

% val1 = v1(1).*(x-segment(end,1)) + v1(2).*(y-segment(end,2)) + v1(3).*(z-segment(end,3));
% val2 = v2(1).*(x-segment(1,1)) + v2(2).*(y-segment(1,2)) + v2(3).*(z-segment(1,3));


val = val1>0;
mask(I) = ~val;

% WriteRAWandMHD(mask, 'mask','C:\Rec',[1 1 1]);

% mask = fast_marching <inf;
end


function [file_name ,seed_point_head]= extract_trace_from_segmentation(folder_path, file_prefix, time_point, seed_point)
    close all;
    %{
    % FIXED PARAMETERS
    %}

    %Parameters FASTMARCHING
    nb_iter_max = 50000000; %number maximum of iteration for fast_marching
    
    % Creating file names
    file_name = [file_prefix '_TP' sprintf('%04d', time_point) '_DC_segmentation']; 
    
    fast_marching_fileName = [file_name '_fM'];
    
    folder_traces_output = fullfile(folder_path,"trace_swc");
    
    fprintf(['\nProcessing \n' file_name]);
    %%% create a folder to save images
    if not(exist(folder_traces_output,'dir'))
        mkdir(folder_traces_output);
    end
    
    %Reading the probability volume
    [Segmentation, ~ ]= readStack(folder_path,file_name);

    % Segmentation correspond to probability values in range [0, 255].
    % Convert to binary mask
    Segmentation = Segmentation > 100;
    
    file_namePrev = [file_prefix '_TP' sprintf('%04d', time_point) '_DC_segmentation'];
    if  exist(fullfile(folder_path,[file_namePrev '_LogN_rec_FM.swc']),'file')
        %taking previous seed point as a prior knowledgue to detect current seed point
        SWC =readSWC(fullfile(folder_path,[file_namePrev '.swc']));

        seed_point = SWC(1,3:5)';
    end
    
    %get sperm's head position
    seed_point = getHeadPosition(Segmentation, seed_point);
    % seed_point = [300 126 16]';
    seed_point_head = seed_point;
   
    % CREATE COST FUNCTION
    Segmentation_Dilated = imdilate(Segmentation, ones(3,3,3));
    Distance_Transform = bwdist(not(Segmentation_Dilated));    
    %CostFunction= Distance_Transform/max(Distance_Transform(:)); 
    CostFunction = exp(Distance_Transform).*Segmentation_Dilated;
    
    %running fast marching
    [fast_marching, ~] = compute_fast_marching(Segmentation_Dilated, CostFunction, seed_point, [-1;-1;-1], 100000, nb_iter_max, folder_path, fast_marching_fileName , true, [1 1 1]);
    [S, ~] = compute_fast_marching(Segmentation_Dilated, Segmentation_Dilated, seed_point, [-1;-1;-1], 100000, nb_iter_max, folder_path, fast_marching_fileName , true, [1 1 1]);    
    

    % Get the fasthest point from the fast marching
    I = S==inf;
    S(I)=0;
    [~,index] = max(S(:));
    [x,y,z] = ind2sub(size(S),index);
    end_points = [x,y,z]';
    S(I)=inf;

    % extract centerline bu backpropagation 
    [a,~] = traceBack_centerline3D([], seed_point, end_points, fast_marching,[], folder_path, fast_marching_fileName); clear fast_marching S;
    
    %saving segments
    trace_coordinates{1} = a{1};
    idx = sub2ind(size(Distance_Transform),trace_coordinates{1}(:,1),trace_coordinates{1}(:,2),trace_coordinates{1}(:,3));
    radius{1} = Distance_Transform(idx);


    %creating the SWC file
    createSWCfromSegments(trace_coordinates, radius, folder_traces_output, [file_name '.swc'], [1 1 1]);
    SWCtoVTK(folder_traces_output, [file_name '.swc']);
    
    % Delete temporal files
    delete_RAW(folder_path,fast_marching_fileName);    

    figure;set(gcf,'Visible', 'off'); 
    imshow(max(Segmentation,[],3)',[]); colormap('gray');hold on;
    plot(trace_coordinates{1}(:,1),trace_coordinates{1}(:,2),'r', 'LineWidth',2);

    print(gcf,fullfile(folder_traces_output, [file_name '.png']),'-dpng')
    close all;
end

function headPos = getHeadPosition(B,seed_point)
    radius = 2;
    
    % flagellum has approximate radius equal to two. Remove flagellum
    B = imerode(B,ones(2*radius,2*radius,2*radius));

    min_size = 5;

    conComp = bwconncomp(B,26);
 
    min_dist = inf;
    
    for i=1:conComp.NumObjects
        if length(conComp.PixelIdxList{i})>min_size
             [I,J,K] = ind2sub(size(B),conComp.PixelIdxList{i});
             X = round(mean(I));
             Y = round(mean(J));
             Z = round(mean(K));
             dist_ = sqrt((X-seed_point(1))^2 + (Y-seed_point(2))^2 +(Z-seed_point(3))^2);

            if (dist_<40 )                
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
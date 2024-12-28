function trace_centerline_from_binary_image()
    close all
    folder_path = 'C:\Users\jalip\Documentos\Proyectos\Sperm\campo_claro_test\2017_11_09_HIGH_VISCOCITY_DONE\2017_11_09_HIGH_VISCOCITY_DONE\Exp13_stacks\output';

    folder_output_images= fullfile(folder_path, 'images');
    folder_output_traces= fullfile(folder_path, 'traces');
    mkdir(folder_output_images)
    mkdir(folder_output_traces)
    
    file_paths = dir(fullfile(folder_path,'*.tif'));

    %Parameters for fast-marching algorithm
    stop_points = [-1;-1;-1]; %stop fast marching if it reaches this point. Hence, never stop
    nb_iter_max = 300*300*100; %stop fast marching if it has already visited this number of points
    current_length = 1000000; %stop fast marching if the length of the structure is larger than current length 

    for i=1:length(file_paths)
        B = readStack(folder_path,file_paths(i).name);
        %segmentation of probability values
        B = B>127;

        head_pos = get_head_position(B);

        CostFunction = bwdist(not(B));

        CostFunction(:) = normalizeVol(double(CostFunction(:)), 0, 1);
        CostFunction = exp(5*CostFunction);

        %running fast marching
        [fast_marching, ~]= front_propagation_double_stopLength(double(CostFunction), single(head_pos-1),single(stop_points-1),nb_iter_max,B>0, current_length); 
        fast_marching(not(B>0)) = inf;

        I =  fast_marching>10000; fast_marching(I) = -0.01;
        [val, index]= max(fast_marching(:));
        fast_marching(I)=inf;

        k = 1;

        figure;set(gcf,'Visible', 'off'); imshow(max(B,[],3)',[]);colormap('gray');hold on;
        plot(head_pos(1,:),head_pos(2,:),'*m', 'LineWidth',2);
        while val>0
            [x,y,z] = ind2sub(size(fast_marching),index);
            end_points = [x,y,z]';

            %extract centerline
            [trace,~] = traceBack_OR1_P([],head_pos,end_points,fast_marching,[],folder_path,[]); 
            %we dont have information about the radius
            radius{1} = 0*trace{1}(:,1);

            plot(trace{1}(:,1),trace{1}(:,2),'r', 'LineWidth',2);

            %creating the SWC file
            createSWCfromSegments(trace, radius, folder_output_traces, [file_paths(i).name '_rec_FM' '_trace_' num2str(k) '.swc'], [1 1 1]);
%             SWCtoVTK(folder_output_traces, [file_paths(i).name '_rec_FM' '_trace_' num2str(k) '.swc']);            

            B = remove_binary_connected(B, index);
            fast_marching = fast_marching.*B;

            I =  fast_marching>10000; fast_marching(I) = -0.01;
            [val, index]= max(fast_marching(:));
            fast_marching(I)=inf;
            k = k+1;
        end
        print(gcf,fullfile(folder_output_images, [file_paths(i).name '_rec.png']),'-dpng')

    end
end

function B2 = remove_binary_connected(B, ind)
    B2 = zeros(size(B));

    conComp = bwconncomp(B,6);
    for i=1:conComp.NumObjects
         if isempty(find(ind == conComp.PixelIdxList{i}))
             B2(conComp.PixelIdxList{i})=1;
         end
    end   
end


function head_pos = get_head_position(B)
    r = 5;
    [xx,yy,zz] = ndgrid(-r+1:r+1);
    nhood = sqrt(xx.^2 + yy.^2 + zz.^2) <= r;

    B = imerode(B,nhood);

    conComp = bwconncomp(B,6);

    head_pos = zeros(3, conComp.NumObjects);
    for i=1:conComp.NumObjects
         [I,J,K] = ind2sub(size(B),conComp.PixelIdxList{i});
         X = round(mean(I));
         Y = round(mean(J));
         Z = round(mean(K));            
         head_pos(:,i) = [X,Y,Z]';
    end    

end
function f09_convert_traces_to_micron_and_smooth()

    %parameters
    folder_path = 'D:\Descargas\Servicio social Dr. Paul\Exp2_stacks\stacks_constant_sampling';
    stack_name_prefix = 'Exp2_stacks';
    stacks_index_to_trace = 1:556;
    folder_path_swc = folder_path;
    objective = 100;
    invert_Y_axis_from_traces = true;

  
    smoothing = [0.0001 0.001];
%     smoothing = [0.0001];
    
    %running algorithm
    spacing_xy = (118/640)*(60/objective); %Value obtained by Corkidi using a ruler, the microscopy objective must not change because it will also change the spacing
    warning(['Pixel resolution x,y = ' num2str(spacing_xy) '. Value obtained by Corkidi using a ruler and 60X objective, if the microscopy objetive changes then this value is not valid.']);
    
    %running code
    folder_out = fullfile(folder_path, 'trace_micras');
    
    folder_out_images = fullfile(folder_out, 'images_traces_interpolated_xy');
    
    if not(exist(folder_out_images,'dir'))
        mkdir(folder_out_images);
    end
    
    %folders to save traces in micras
    folder_out_raw = fullfile(folder_out,'raw');
    if not(exist(folder_out_raw,'dir'))
        mkdir(folder_out_raw);
    end
    
    for i=1:length(smoothing)
        folder_out_smooth{i} = fullfile(folder_out,'trace_smooth', ['trace_micras_smooth_' num2str(smoothing(i))]);
        if not(exist(folder_out_smooth{i},'dir'))
            mkdir(folder_out_smooth{i});
        end
    end   
    
    tj = 1;
    for stackID = stacks_index_to_trace          
        
        ID = get_TPID(stackID);

        file_name_swc = [stack_name_prefix '_' ID '_DC_trace.swc'];
        file_name_txt = [stack_name_prefix '_' ID '.txt'];
        
        zval = load(   fullfile(folder_path,file_name_txt));
        SWC  = readSWC(fullfile(folder_path_swc,file_name_swc));

        if invert_Y_axis_from_traces
            warning('Inverting Y-axis to have the correct position in real space. Images invert Y-axis')
            SWC(:,4) = 480-SWC(:,4);
        end

        %just to make sure that the z value is inside stack
        I = SWC(:,5)>length(zval);
        SWC(I,5)=length(zval);
        if sum(I)>0
            warning (['Truncating z values for file ' file_name_swc ]);
        end
        
        %updating Z values (integer) to micrometer values 
        SWC(:,5)=zval(SWC(:,5));


        %converting xy voxel coordinates to micrometers
        SWC(:,3:4)= spacing_xy*SWC(:,3:4);



        %interpolating to have equidistant distance between points and the
        %same number of points --- smoothing = 1, means no  apply smooth
        points_interpolated = smooth_to_constant_number_points(SWC(:,3:5), 100, 1);
        swc_interpolated  = points_to_SWC(points_interpolated);
        
        dlmwrite(fullfile(folder_out_raw,[stack_name_prefix  '_' ID  '_micras.swc']), swc_interpolated, 'delimiter', ' ','precision',6);
%         SWCtoVTK_RAM(folder_out_raw, [stack_name_prefix  '_TP' ID  '_micras.swc'],SWC)

        X_raw(:,tj) = swc_interpolated(:,3);
        Y_raw(:,tj) = swc_interpolated(:,4);
        Z_raw(:,tj) = swc_interpolated(:,5);
        
        h = figure;set(gcf,'Visible', 'off'); 
        labels = [];
        plot(points_interpolated(:,1),points_interpolated(:,2),'g','LineWidth',2);
        labels{1} = 'raw';
        hold on        

        for i=1:length(smoothing)
            labels{length(labels)+1} = ['s = ' num2str(smoothing(i))];
            %SMOOTHING THE CENTERLINE
            points_smooth = smooth_to_constant_number_points(SWC(:,3:5), 100, smoothing(i));
            plot(points_smooth(:,1),points_smooth(:,2),'LineWidth',2);
            swc_smooth  = points_to_SWC(points_smooth);
            dlmwrite(fullfile(folder_out_smooth{i},[stack_name_prefix  '_' ID  '_smooth.swc']),swc_smooth, 'delimiter', ' ','precision',6);
            X_smooth{i}(:,tj) = swc_smooth(:,3);
            Y_smooth{i}(:,tj) = swc_smooth(:,4);
            Z_smooth{i}(:,tj) = swc_smooth(:,5);
%             SWCtoVTK_RAM(folder_out_smooth{i}, [stack_name  '_TP' ID  '_smooth.swc'],SWC_smooth)
        end
%         xlim([0 640*spacing_xy]);
%         ylim([0 480*spacing_xy]);
        axis('equal');
        legend(labels);
        print(gcf,fullfile(folder_out_images, [stack_name_prefix  '_' ID '_traces.png']),'-dpng') 
        close(h);
        tj =tj+1;
    end
    
    %saving data
    file_save = fullfile(folder_out,[stack_name_prefix '_traces_raw.mat']);
    save(file_save,'X_raw','Y_raw','Z_raw', 'stack_name_prefix', 'stacks_index_to_trace');
    
    for i=1:length(smoothing)
        %saving data
        file_save = fullfile(folder_out,[stack_name_prefix '_traces_smooth_p_' num2str(smoothing(i)) '.mat']);
        X = X_smooth{i}; Y = Y_smooth{i}; Z = Z_smooth{i};
        save(file_save,'X','Y','Z', 'stack_name_prefix', 'stacks_index_to_trace');
    end    
end

function points_interpolated = smooth_to_constant_number_points(points, n, penalization)
    %penalization = 1 means no smoothing
    %get the x,y,z coordinates
    xr = points(:,1)';
    yr = points(:,2)';
    zr = points(:,3)';

    pp = penalization; % 1= interpolation without cubic spline
    ppz = penalization;

%     sold = arclength(xr', yr', zr');
    sold = 1:length(xr);
    snew = linspace(0,sold(end),n)';

    X = fnval(csaps(sold,xr',pp),snew);
    Y = fnval(csaps(sold,yr',pp),snew);
    Z = fnval(csaps(sold,zr',ppz),snew); 
    
    points_interpolated = [X Y Z];
end
    
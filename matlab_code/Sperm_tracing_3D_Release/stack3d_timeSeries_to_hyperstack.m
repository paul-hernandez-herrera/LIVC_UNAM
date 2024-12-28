function stack3d_timeSeries_to_hyperstack()
    folder_path = 'C:\Users\jalip\Documentos\Proyectos\Sperm\Campo_claro\2021_10_08 100x-80hzs-20 micras-8000fps\Exp6_stacks';
    stack_name_prefix  = 'Exp6_stacks';

%     overwrite = true;
    
    [n_frames,slices] = get_hyperstack_parameters(folder_path, stack_name_prefix); 
    
    hyperstack = [];
    
    
    im_n = 1;
    for tp=0:999

        file_name = get_file_name(folder_path, stack_name_prefix, tp);  

        if not(isempty(file_name))
            V = readStack(folder_path,file_name);

            if isempty(hyperstack)
                hyperstack = zeros(size(V,1),size(V,2), n_frames*slices,'uint8');
            end
            hyperstack(:,:,im_n:im_n+slices-1) = V;
            im_n = im_n + slices;
%             write_tif(V,folder_path,[stack_name_prefix '_hyperstack' '_nSlices_' num2str(slices) '_nFrame_' num2str(n_frames) ],overwrite);
%             if overwrite
%                 overwrite = false;
%             end
        end
    end
    
    WriteRAWandMHD(hyperstack, [stack_name_prefix '_hyperstack' '_nSlices_' num2str(slices) '_nFrame_' num2str(n_frames) ],folder_path)
end

function [n_frames,slices] = get_hyperstack_parameters(folder_path, stack_name_prefix)

    n_frames =  0 ;
    V = [];
    for tp=0:999

        file_name = get_file_name(folder_path, stack_name_prefix, tp); 

        if not(isempty(file_name))
            if isempty(V)
                V = readStack(folder_path,file_name);
                [~,~,slices] =size(V);
            end
            n_frames = n_frames + 1;
        end
    end
    
end

function write_tif(imageStack,folder_path,file_name,overwrite)

    full_folder_path = fullfile(folder_path,[file_name '.tif']);

    numberOfImages = size(imageStack,3);
    for k = 1:numberOfImages
        currentImage = imageStack(:,:,k);
        currentImage = currentImage';

        if (overwrite)
            imwrite(currentImage,full_folder_path,'tif', 'WriteMode','overwrite');
            overwrite=false;
        else
            imwrite(currentImage,full_folder_path,'tif', 'WriteMode','append');
        end
    end 

end

function file_name = get_file_name(folder_path, stack_name_prefix, tp)
    
    file_name = [];
    
    id_str = tp_to_string(tp);
    if exist(fullfile(folder_path, [stack_name_prefix '_TP' id_str '_DC.mhd']),'file')
        file_name = [stack_name_prefix '_TP' id_str '_DC'];
    elseif exist(fullfile(folder_path, [stack_name_prefix '_TP' id_str(2:end) '_DC.mhd']),'file')
        file_name = [stack_name_prefix '_TP' id_str(2:end) '_DC'];
    end
    
end

function ID = tp_to_string(currentTP)

    if (currentTP<10)
        ID = ['000' num2str(currentTP)];
    elseif (currentTP<100)
        ID = ['00' num2str(currentTP)];
    elseif (currentTP<1000)
        ID = ['0' num2str(currentTP)];
    elseif (currentTP<10000)
        ID = num2str(currentTP);    
    end

end

function WriteRAWandMHD(X, filePrefix,relpativePath,spacingOut)

    %Checks Spacing
    if (~exist('spacingOut','var'))
        spacingOut=[1 1 1];
    end     
    
    %just to remove the extension of the mhd file
    if length(filePrefix)>=3
        if strcmp(filePrefix(end-3:end),'.mhd')
            filePrefix(end-3:end) = [];
        end
    end
    
    mhdFile = [ filePrefix '.mhd' ];
    rawFile = [ filePrefix '.raw' ];
    
    elType = class(X);
    switch elType
        case 'int16'
            elTypeOut.mhd = 'MET_SHORT';
        case 'uint8'
            elTypeOut.mhd = 'MET_UCHAR';
            elTypeOut.vvi =  3;                        
        case 'uint16'
            elTypeOut.mhd = 'MET_USHORT';
            elTypeOut.vvi =  5;              
        case 'uint32'
            elTypeOut.mhd = 'MET_ULONG';
            elTypeOut.vvi =  9;                          
        case 'single'
            elTypeOut.mhd = 'MET_FLOAT';
            elTypeOut.vvi =  8;            
        case 'double'
            elTypeOut.mhd = 'MET_DOUBLE';
            elTypeOut.vvi =  8;      
        case 'logical'
            elTypeOut.mhd = 'MET_UCHAR';
            elTypeOut.vvi =  3;                                    
        otherwise
            outstr = sprintf('Data type unknown ("%s") - please modify WriteRAWandMHD.', elType);
            error(outstr);
    end
    % Open file in the destination
    % Relative path. Alberto Jan 2006
    if (exist('relpativePath','var'))
        mhdFileWithPath =  fullfile( relpativePath,mhdFile );        
        mhd = fopen(mhdFileWithPath, 'wt');                        
    else
        mhd = fopen(mhdFile, 'wt');            
    end   
    %Write mhd file
    fprintf(mhd, 'ObjectType = Image\n');
    fprintf(mhd, 'NDims = 3\n');
    fprintf(mhd, 'BinaryData = True\n');
    fprintf(mhd, 'BinaryDataByteOrderMSB = False\n');
    fprintf(mhd, 'ElementSpacing =  %g  %g   %g \n', spacingOut(1), spacingOut(2), spacingOut(3));    
    fprintf(mhd, 'DimSize = %d %d %d\n', size(X,1), size(X,2), size(X,3));
    fprintf(mhd, 'ElementType = %s\n', elTypeOut.mhd);
    fprintf(mhd, 'ElementDataFile = %s\n', rawFile);
    fclose(mhd);

    %Write raw file
    % Relative path. Alberto Jan 2006
    if (exist('relpativePath','var'))
        rawFileWithPath =  fullfile( relpativePath,rawFile );    
        raw = fopen(rawFileWithPath, 'wb');                        
    else
        raw = fopen(rawFile, 'wb');    
    end   
    fwrite(raw, X, class(X)); 
    fclose(raw);
%     clear all;
    
end


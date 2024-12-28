function [stack,SPACING] = readStack(file_path,file_name)
[~,name,ext] = fileparts(file_name);
if (exist(fullfile(file_path,[file_name '.mhd']),'file'))
    [stack,SPACING] = RAWfromMHD(file_name,[],file_path);
elseif(exist(fullfile(file_path,[file_name '.tif']),'file'))
    stack = read_tif(file_path,[file_name '.tif']);
    SPACING = [1 1 1];    
elseif (ext==".tif")
    stack = read_tif(file_path,[name '.tif']);
    SPACING = [1 1 1];        
else 
    warning('File not found');
    stack = [];
end


end
function delete_RAW(file_path,file_name)
%function to delete RAW and MHD files

%deleting raw file if it is found
if exist(fullfile(file_path,[file_name '.raw']),'file')
    delete(fullfile(file_path,[file_name '.raw']));
end

%delete mhd file if it is found
if exist(fullfile(file_path,[file_name '.mhd']),'file')
    delete(fullfile(file_path,[file_name '.mhd']));
end
end
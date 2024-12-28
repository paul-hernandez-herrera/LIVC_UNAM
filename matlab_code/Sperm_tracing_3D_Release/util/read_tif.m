function imageStack=read_tif(file_path,file_name)

full_file_path = fullfile(file_path,file_name);

info = imfinfo(full_file_path);
numberOfImages = length(info);
for k = 1:numberOfImages
    currentImage = imread(full_file_path, k, 'Info', info);
    if k==1
        imageStack = zeros([size(currentImage,2),size(currentImage,1),numberOfImages],class(currentImage));
    end
    imageStack(:,:,k) = currentImage(:,:,1)';
end 

end
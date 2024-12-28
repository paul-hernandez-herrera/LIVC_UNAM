function display_Projections_xy_xz_yz(folder_path,stack_name_prefix)
%display the proyections in the XY,XZ and YZ plane
fprintf('Saving projections ... \n');
file_out = fullfile(folder_path,'Stack_projections_xy_xz_yz');
if not(exist(file_out,'dir'))
    mkdir(file_out);
end


make_it_tight = true;
subplot = @(m,n,p) subtightplot (m, n, p, [0.01 0.05], [0.1 0.01], [0.1 0.01]);
if ~make_it_tight,  clear subplot;  end

for stackID=1:999
    close all;
    ID = get_TPID(stackID);
    
    
    current_file = [stack_name_prefix '_' ID];
    
    if exist(fullfile(folder_path,[current_file '.mhd']),'file') 
%         fprintf('\n\n')
%         tic
        V = readStack(folder_path,current_file);
        V = V(2:2:end,2:2:end,:);
        %correctling light ilumination
        
        V = V - imclose(imopen(V,ones(5,5,1)),ones(5,5,1));
        
        
        
        
        reSampleFactor=3;
        figure;set(gcf,'Visible', 'off'); 
        im_pro = max(single(V),[],3);
        
        h = subaxis(3,1,1,'SpacingVert',0,'MR',0,'Holdaxis'); imshow(im_pro,[]);colormap('gray');hold on; title('Projection XY');set(h,'position',[0.02 0.35 0.35 0.35]);
        
        
        im_pro = max(single(V),[],1); im_pro=reshape(im_pro,[size(im_pro,2) size(im_pro,3)])';
        im_pro = im_pro(end:-1:1,1:end);
        im_pro = imresize(im_pro,[reSampleFactor*size(im_pro,1) size(im_pro,2)]) ;
        h = subaxis(3,1,2,'SpacingVert',0,'MR',0,'Holdaxis'); imshow(im_pro,[]);colormap('gray');hold on;title('Projection XZ'); set(h,'position',[0.40 0.55 0.40 0.40]);  
        
        im_pro = max(single(V),[],2); im_pro=reshape(im_pro,[size(im_pro,1) size(im_pro,3)])';
        im_pro = im_pro(end:-1:1,end:-1:1);
        im_pro = imresize(im_pro,[reSampleFactor*size(im_pro,1) size(im_pro,2)]) ;
        l = size(V,1)/size(V,2);
        h=subaxis(3,1,3,'SpacingVert',0,'MR',0,'Holdaxis'); imshow(im_pro,[]);colormap('gray');hold on; title('Projection YZ');set(h,'position',[0.40 0.05 l*0.40 l*0.40]); 

        
        print(gcf,fullfile(file_out, [current_file '_projections_3D.png']),'-dpng')   
         
%         toc      
        
    end
end
fprintf('Done \n');
end
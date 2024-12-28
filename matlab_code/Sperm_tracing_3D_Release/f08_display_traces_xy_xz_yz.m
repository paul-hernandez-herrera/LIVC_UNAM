function f08_display_traces_xy_xz_yz(folder_path, stack_name_prefix, stacks_index_to_trace)

%parameters
% folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp17_stacks\stacks_constant_sampling';
% stack_name_prefix = 'Exp17_stacks';
% stacks_index_to_trace = 1:273;

%running the function
file_out = fullfile(folder_path,'trace_projections_xy_xz_yz');
if not(exist(file_out,'dir'))
    mkdir(file_out);
end


length_border = 40;
make_it_tight = true;
% subplot = @(m,n,p) subtightplot (m, n, p, [0.01 0.05], [0.1 0.01], [0.1 0.01]);
% if ~make_it_tight,  clear subplot;  end
for stackID= stacks_index_to_trace
    close all;
    ID = get_TPID(stackID);
    
    
    current_file = [stack_name_prefix '_' ID '_DC'];
    current_name_SWC = [current_file '_trace.swc'];
    
    if exist(fullfile(folder_path,current_name_SWC),'file')         
        V = readStack(folder_path,current_file);
        SWC = readSWC(fullfile(folder_path,current_name_SWC));
        

        swc_minx= round(min(SWC(:,3))-length_border);if (swc_minx<1); swc_minx=1;end
        swc_maxx= round(max(SWC(:,3))+length_border);if (swc_maxx>size(V,1)); swc_maxx=size(V,1);end
        swc_miny= round(min(SWC(:,4))-length_border);if (swc_miny<1); swc_miny=1;end
        swc_maxy= round(max(SWC(:,4))+length_border);if (swc_maxy>size(V,2)); swc_maxy=size(V,2);end
        V2 = single(V(swc_minx:swc_maxx,swc_miny:swc_maxy,:));  
        V2(:) =normalizeVol(V2(:),0,255); 
        V = V2;
        V = log(V+1);
%         s_stack = size(V);
        
        SWC(:,3) = SWC(:,3)-swc_minx+1;
        SWC(:,4) = SWC(:,4)-swc_miny+1;
        
        
        reSampleFactor=3;
        SWC(:,3:5) = SWC(:,3:5);
        figure;set(gcf,'Visible', 'off'); 
        im_pro = max(single(V),[],3);I = im_pro==0; im_pro(I) = min(im_pro(not(I)));
        
        subplot(3,2,1); 
        imshow(im_pro,[]);colormap('gray');hold on; t=title('Projection XY');%set(h,'position',[0.02 0.50 0.35 0.35]);
        subplot(3,2,2); imshow(im_pro,[]);colormap('gray');hold on;plot(SWC(:,4),SWC(:,3),'r', 'LineWidth',2.5);%set(h,'position',[0.52 0.50 0.35 0.35]);
        
        
        im_pro = max(single(V),[],1); im_pro=reshape(im_pro,[size(im_pro,2) size(im_pro,3)])';
        im_pro = im_pro(end:-1:1,1:end); I = im_pro==0; im_pro(I) = min(im_pro(not(I)));
        im_pro = imresize(im_pro,[reSampleFactor*size(im_pro,1) size(im_pro,2)]) ;
        h = subplot(3,2,3); imshow(im_pro,[]);colormap('gray');hold on;title('Projection XZ'); %set(h,'position',[0.1 0.26 0.20 0.20]);  
        h=subplot(3,2,4); imshow(im_pro,[]);colormap('gray');hold on;plot(SWC(:,4),reSampleFactor*(size(V,3)-SWC(:,5)),'r', 'LineWidth',2.5); %set(h,'position',[0.6 0.26 0.20 0.20]);  
%         set(hax);
        
        im_pro = max(single(V),[],2); im_pro=reshape(im_pro,[size(im_pro,1) size(im_pro,3)])';
        im_pro = im_pro(end:-1:1,end:-1:1);I = im_pro==0; im_pro(I) = min(im_pro(not(I)));
        im_pro = imresize(im_pro,[reSampleFactor*size(im_pro,1) size(im_pro,2)]) ;
        SWC(:,3) = size(V,1)-SWC(:,3);
        SWC(:,5) = size(V,3)-SWC(:,5);
        l = size(V,1)/size(V,2);
        h=subplot(3,2,5); imshow(im_pro,[]);colormap('gray');hold on; title('Projection YZ');%set(h,'position',[0.035 -0.03 l*0.25 l*0.25]); 
        h=subplot(3,2,6); imshow(im_pro,[]);colormap('gray');hold on;plot(SWC(:,3),reSampleFactor*SWC(:,5),'r', 'LineWidth',2.5);%set(h,'position',[0.535 -0.03 l*0.25 l*0.25]); 
        
        print(gcf,fullfile(file_out, [current_file '_projections.png']),'-dpng')   
      
    end
end
end
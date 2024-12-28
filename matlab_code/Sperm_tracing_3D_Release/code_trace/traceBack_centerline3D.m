function [segment,radius] = traceBack_centerline3D(WProjection,startPoint,terminalPoints,fastMarching,C_P,file_path,fNameOutDistanceMap)
%figure;imshow(max(fastMarching,[],3)',[]);colormap('jet');hold on;
%removing indices that were not reached by the fastMarching
show_images = false;

%converting to index the terminal points
if ~isempty(terminalPoints)
    terminalPoints_ind = sub2ind(size(fastMarching),terminalPoints(1,:),terminalPoints(2,:),terminalPoints(3,:));
    I = fastMarching(terminalPoints_ind)<=0;
    terminalPoints_ind(I) = [];
else
    terminalPoints_ind = [];
end



%giving high values outside the fastMarching to allow the minimum to
%propagate inside the dendrite
% max_FM = 1.001*max(fastMarching(:));
% fastMarching(fastMarching<=0) = max_FM;
max_FM = inf;

if show_images
    figure;
    imshow(WProjection',[],'InitialMagnification','fit');
    hold on;
end

for i=1:size(startPoint,2)
    fastMarching(startPoint(1,i),startPoint(2,i),startPoint(3,i)) = 0;
end

segment = [];

radius = [];

Neigh = createNeighboorhs;

total_centerline_points = [];

%reading distanceMap
if ~isempty(fNameOutDistanceMap)
    DT = RAWfromMHD(fNameOutDistanceMap,[],file_path);
else
    DT = ones(size(fastMarching),'single');
end

while ~isempty(terminalPoints_ind)
    %get position of the max value in the seed points
    [val,pos] = max(fastMarching(terminalPoints_ind));
    
    %index for the current terminal point to extract the centerline
    current_ind = terminalPoints_ind(pos(1));
    
    %removing the current terminal point
    terminalPoints_ind(pos(1)) = [];
    
%     fastMarching(current_ind)=val(1)+1;
    [segment,radius,current_ind] = getPathFromTerminalPoint(Neigh,val,max_FM,fastMarching,segment,radius,current_ind,DT,show_images);
%     fastMarching(current_ind)=val(1);
    %plot(segment{end}(:,1),segment{end}(:,2),'g.')
    
    %setting value to zero to the current segment to allow stop the
    %backpropagation.
    fastMarching(current_ind)=0;
    
    %all the points in the centerline
    total_centerline_points = [total_centerline_points;segment{end}];

end


if show_images
    %just to plot the centerline
    seed_P  = startPoint(:,1)';
    for i=1:length(segment)
        if ~isempty(intersect(segment{i},seed_P,'rows'))
            seed_P  = [seed_P; segment{i}];
            plot(segment{i}(:,1),segment{i}(:,2),'g','LineWidth',3)
        else
            plot(segment{i}(:,1),segment{i}(:,2),'b','LineWidth',3)
        end
    end
end


if ~isempty(C_P)
    I = sub2ind(size(fastMarching), C_P(:,1),C_P(:,2),C_P(:,3));
    all_radii = DT(I);
    threshold = 2*(mean(all_radii)+std(all_radii)); 
    threshold = (mean(all_radii)+std(all_radii)); 
end

current_centerline_points = total_centerline_points;
while ~isempty(C_P)
    if ~isempty(current_centerline_points)
        %just to remove the points in C_P than are close to the detected
        %points in the centerline
        D = pdist2(double(current_centerline_points),double(C_P),'euclidean','Smallest',1)';
        I = D<=threshold;
        C_P(I,:) = [];
    end
    %fprintf('%i\n',size(C_P,1));
    if ~isempty(C_P)
        I = sub2ind(size(fastMarching), C_P(:,1),C_P(:,2),C_P(:,3));
        values = fastMarching(I);
        [val,index_] = max(values);
        current_ind = I(index_(1));
        
        %get the path for current index
        [segment,radius,current_ind] = getPathFromTerminalPoint(Neigh,val,max_FM,fastMarching,segment,radius,current_ind,DT,show_images);

        if show_images
            %just to plot the current segment
            plot(segment{end}(:,1),segment{end}(:,2),'r','LineWidth',3);
        end

        %setting value to zero to the current segment to allow stop the
        %backpropagation.
        fastMarching(current_ind)=0;

        %all the points in the centerline
        current_centerline_points = segment{end};
    end 
end
%plot3(path(:,1)-3,path(:,2)-3,path(:,3)-3,'g.')
end

function [segment,radius,current_ind] = getPathFromTerminalPoint(Neigh,val,max_FM,fastMarching,segment,radius,current_ind,DT,show_images)
%getting the size of the volume
max_it = 10000;

size_fastMarching = size(fastMarching);
%getting the 3D coordinates of the current terminal points
[x,y,z] = ind2sub(size_fastMarching,current_ind);

%creating a new cell for the new path
idS = length(segment) + 1;
segment{idS} = [x y z];

radius{idS} = DT(x,y,z);

if show_images
    plot(x,y,'yo','lineWidth',3,'markerSize',10);
end

%fastMarching(x,y,z) = max_FM;

%setting the previous value as the maximum of the fast_marching
previous_val = max_FM;

it =0;
while val>0 &&  val <= previous_val && it<max_it
    it = it +1;
    %setting the previous value as the last minimum
    previous_val = val;

    if previous_val == inf
        fprintf('\nCurrent_value infinite\n');
        break;
    end

    %creating neighboors of the current point
    currentNeighboorhs = [x+Neigh(:,1) y+Neigh(:,2) z+Neigh(:,3)];
    
    %to have good boundary conditions;
    I = currentNeighboorhs(:,1)<=0 | currentNeighboorhs(:,2)<=0 | currentNeighboorhs(:,3)<=0 ...
        | currentNeighboorhs(:,1)>size_fastMarching(1) | currentNeighboorhs(:,2)>size_fastMarching(2) | currentNeighboorhs(:,3)>size_fastMarching(3);
    currentNeighboorhs(I,1) = x;currentNeighboorhs(I,2) = y;currentNeighboorhs(I,3) = z;
    
    
    I = sub2ind(size_fastMarching, ...
        currentNeighboorhs(:,1),currentNeighboorhs(:,2),currentNeighboorhs(:,3));
    
    %getting the minimum value from the fastmarching in the neighboorhod
    [val,iMin] = min(fastMarching(I));

    %getting the coordinated of the point to backpropagate
    x=currentNeighboorhs(iMin(1),1); y=currentNeighboorhs(iMin(1),2); z=currentNeighboorhs(iMin(1),3);

%     fastMarching(x,y,z) = inf;
    segment{idS} = [x y z;segment{idS}];
    radius{idS} = [DT(x,y,z);radius{idS}];
    
    current_ind = [current_ind;I(iMin(1))];
end

end

function Neigh = createNeighboorhs
%function to create a 26 neighborhod
Neigh = [];
for i =-1:1
    for j=-1:1
        for k=-1:1
            if (i~=0 || j~=0 || k~=0)
                Neigh = [Neigh; i,j, k];
            end
        end
    end
end


end
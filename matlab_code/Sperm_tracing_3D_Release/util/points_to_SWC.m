function new_SWC  = points_to_SWC(points)
%function that allows to save the points in a volume

%creating the new segment
new_SWC = zeros(size(points,1),7);
new_SWC(:,1) = 1:size(points,1);
new_SWC(:,7) = new_SWC(:,1) - 1;
new_SWC(:,3:5) = points;
new_SWC(:,6) = 1;
new_SWC(1,7) = -1;
    
end
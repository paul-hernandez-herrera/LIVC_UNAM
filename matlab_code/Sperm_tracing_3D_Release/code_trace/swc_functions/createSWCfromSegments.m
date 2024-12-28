function createSWCfromSegments(segments,radius,file_path,file_output,spacing)
%function that allows to create the SWC from the segments of the
%centerline.
current_segment = segments{1};
current_radius = radius{1};

%current_number_of_disconnected_components 
disconected_ID = -1;

%creating a variable for the first segment
SWC = ones(size(current_segment,1),7);
%ID
SWC(:,1)=1:size(current_segment,1);
%coordinates
SWC(:,3:5) = current_segment(:,1:3);
%radius
SWC(:,6) = current_radius(:,1);
%parent
SWC(1,7) = disconected_ID;
SWC(2:end,7) = SWC(1:end-1,1);

for i=2:length(segments)
    current_segment = segments{i};
    
    current_radius = radius{i};
    
    
    if ~isempty(current_segment)
        %the first row is the child of the current segment
        segment_child = current_segment(1,1:3); 

        %checking if the current child already appear in the SWC file
        [~,child_,~] = intersect(SWC(:,3:5),segment_child,'rows');

        %removing the child if it already appear in a previous segment
        if ~isempty(child_)
            current_segment(1,:) = [];
            current_radius(1,:) = [];
        end

        %creating a variable for the first segment
        Current_SWC = ones(size(current_segment,1),7);
        %ID
        Current_SWC(:,1)=(1:size(current_segment,1))' + size(SWC,1);
        %coordinates
        Current_SWC(:,3:5) = current_segment(:,1:3);
        %radius
        Current_SWC(:,6) = current_radius(:,1);    

        %Just in case that we have at least a point in the current segment
        if ~isempty(Current_SWC)
            %parent
            if isempty(child_)
                %decrease the ID for the disconnected component
                disconected_ID = disconected_ID-1;
                Current_SWC(1,7) = -1;
            else
                Current_SWC(1,7) = child_;
            end
            Current_SWC(2:end,7) = Current_SWC(1:end-1,1);
        end

        %append to the SWC
        SWC = [SWC;Current_SWC];
    end

end

SWC = createIDforSegments(SWC);

dlmwrite(fullfile(file_path,file_output), SWC, 'delimiter', ' ','precision',6);

end
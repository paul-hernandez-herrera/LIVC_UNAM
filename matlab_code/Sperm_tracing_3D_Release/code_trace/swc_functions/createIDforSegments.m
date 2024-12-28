function SWC = createIDforSegments(SWC)
%function that allows to create a different ID for each segment.
SWC = createID(SWC); 
SWC = fix_ordering_of_segments(SWC);
SWC = createID(SWC);

end

function SWC = createID(SWC)

I = detect_connections(SWC);

%creating the IDs for each segment
if length(I)>1

    %creating the ID for the first segment
    SWC(I(1):I(2),2) = 1;

    %creating ID for the remaining segments
    for pos=2:length(I)-1
        SWC(I(pos)+1:I(pos+1),2) = pos;
    end
else
    SWC(:,2)=1;
end

end

function I = detect_connections(SWC)
%detecting branching points
[~,ind_pos_branch]= detectBranchingPointsSWC(SWC);

%detecting terminal points
[~, ind_pos_terminal]= detectTerminalPointsFromSWC(SWC);

%detection roots
ind_pos_roots = find(SWC(:,7)==-1);

%positions where the segments must be partitioned
I = [ind_pos_branch;ind_pos_terminal;ind_pos_roots];

%to reorganized the segment 
% P = SWC(:,7);
% diff_P = [0; diff(P)];
% s_Id = diff_P<0 & P>0;

P = SWC(:,7);
ID = SWC(:,1);
s_Id = (ID-P)>1 & P>0;

I = [I;SWC(s_Id,7)];

I = sort(I);

I = unique(I);

end

% function SWC = move_segment(SWC,diff_P,pos)
% diff_P(1:pos-1)=0;
% 
% I = find(diff_P<0);
% 
% I_2 = detect_connections(SWC);
% I_ind = I_2<=pos;
% I_2(I_ind) = [];
% 
% I = [I;I_2];
% I = sort(I);
% I = unique(I);
% 
% ini_pos = I(1);
% if length(I)>1
%     end_pos = I(2)-1;
% else
%     end_pos = size(SWC,1);
% end
% 
% new_pos = SWC(ini_pos,7)+1;
% 
% current_segment = SWC(ini_pos:end_pos,:);
% 
% segment_length = size(current_segment,1);
% 
% SWC(ini_pos:end_pos,:) = [];
% 
% I = SWC(:,7)==current_segment(end,1);
% SWC(I,7) = inf;
% 
% %updating IDs
% I = SWC(:,1)>=new_pos & SWC(:,1)<ini_pos;
% SWC(I,1) = SWC(I,1) +segment_length;
% 
% %updating parent
% I = SWC(:,7)>=new_pos & SWC(:,7)<ini_pos;
% SWC(I,7) = SWC(I,7) +segment_length;
% 
% %updating the new position for the segement
% current_segment(:,1)= new_pos:new_pos + segment_length - 1;
% current_segment(:,7)= new_pos-1:new_pos + segment_length - 2;
% 
% I = SWC(:,7)==inf;
% SWC(I,7) = current_segment(end,1);
% 
% SWC = [SWC(1:new_pos-1,:); ...
%     current_segment; ...
%     SWC(new_pos:end,:)];
% end

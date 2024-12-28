function SWC = fix_ordering_of_segments(SWC)

I = detect_connections(SWC);

%to reorganized the segment 
Parent = SWC(:,7);
diff_Parent = [0; diff(Parent)];
s_Id = find(diff_Parent<0 & Parent>0);

to_move = [];
for i=1:length(s_Id)
    current_pos = s_Id(i);
    if isempty(find(I == SWC(current_pos,7), 1))
        to_move = [to_move; current_pos];
    end
end

for i =1:length(to_move)
    old_pos = to_move(i);
    new_pos = SWC(old_pos,7)+1;
    SWC = move_segment(SWC,old_pos,new_pos);
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

I = sort(I);

I = unique(I);

end
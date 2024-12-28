function [bp,ind_pos]= detectBranchingPointsSWC(SWC)
%function that allows to extract the branching points from the SWC

%sortting the parents
I = sort(SWC(:,7));

%identifying repited parents (These correspond to the branching points)
diff_I = [-1;diff(I)];
index = diff_I == 0;

%getting the branching points
ind_pos = unique(I(index));

%just removing the roots from the branching points
I = ind_pos ==-1;
ind_pos(I) = [];

%getting the coordinates of the branching points
bp = SWC(ind_pos,3:5);

end
function [terminalPoints, pos]= detectTerminalPointsFromSWC(SWC)
%function to detect the terminal points from the SWC
[~,pos] = setdiff(SWC(:,1),SWC(:,7));

%just to detect if root points are terminal points
I = find(SWC(:,7)==-1);

for i=1:length(I)
    %current position of root point
    c_pos = I(i);
    
    %getting parents
    P = find(SWC(:,7)==c_pos);
    
    %if there is only one parent, the current root point is a terminal
    %point
    if length(P)==1
        %fprintf('Detected root point is a terminal point\n');
        pos = [c_pos;pos];
    end
end

terminalPoints = SWC(pos,3:5);

end
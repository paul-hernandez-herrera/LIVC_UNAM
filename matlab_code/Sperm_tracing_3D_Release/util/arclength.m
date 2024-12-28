% Calculating the tail length 

function [a] = arclength(x,y,varargin)

np = size(x,1); % arclength index
nf = size(x,2);

if length(varargin)>=1
    z  = varargin{1};
    a  = zeros(np,nf);
    
    for t1=1:nf
        for s1=1:np-1
            a(s1+1,t1) = ( (x(s1+1,t1) - x(s1,t1))^2 + (y(s1+1,t1) - y(s1,t1))^2 +...
                (z(s1+1,t1) - z(s1,t1))^2 )^0.5 + a(s1,t1);
        end
    end  
    
else
    
    a  = zeros(np,nf);
    for t1=1:nf
        for s1=1:np-1
           a(s1+1,t1) = ( (x(s1+1,t1) - x(s1,t1))^2 + (y(s1+1,t1) - y(s1,t1))^2)^0.5 + a(s1,t1);
        end
    end
end
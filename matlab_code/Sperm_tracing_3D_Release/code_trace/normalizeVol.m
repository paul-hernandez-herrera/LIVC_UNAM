function vol=normalizeVol(vol,m,M)
%function to normalize the volume such that the minimum and maximum values
%are given at m and M, respectively;

% vol=single(vol);

a = min(vol(:));
b = max(vol(:));
if a~=b
    vol=((M-m)/(b-a)).*vol + (m*b-M*a)/(b-a);  
end
% min(vol(:))
% max(vol(:))
return
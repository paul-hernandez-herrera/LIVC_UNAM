function SWCtoVTK(file_path, file_name)
%function to convert SWC files to VTK format
%Input:
%file_path: the path to the folder which contain the SWC file
%file_name: the name of the SWC file without extension

path_to_file = fullfile(file_path,file_name);

%function to convert an SWC file format to a vtk format
SWC = readSWC(path_to_file);

%getting the points in te centerline
POINTS = SWC(:,3:5);

%Matlab index start at [1 1 1] but C++ start at [0 0 0]. Reducing one
%position in each coordinate
POINTS = POINTS - 1;

%Getting the line connections
CONNECTIONS = [SWC(:,1) SWC(:,7)];

%removing points without connections
I = CONNECTIONS(:,2) == -1;
CONNECTIONS(I,:) = [];
CONNECTIONS = CONNECTIONS-1;

%Adding the required value of the number of conection 
CONNECTIONS = [2*ones(size(CONNECTIONS,1),1) CONNECTIONS];

fid = fopen(strcat(path_to_file, '.vtk'),'w');
fprintf(fid,'# vtk DataFile Version 2.0\n');
fprintf(fid,'# ORIGINAL_SOURCE: Computational Biomedical Lab (CBL)\n');
fprintf(fid,'ASCII\n');
fprintf(fid,'DATASET POLYDATA\n');
fprintf(fid,'POINTS %i float\n',size(POINTS,1));
fprintf(fid,'%2.3f\t %2.3f\t %2.3f\n',POINTS');
fprintf(fid,'LINES %i %i\n',size(CONNECTIONS,1),3*size(CONNECTIONS,1));
fprintf(fid,'%i\t %i\t %i\n',CONNECTIONS');
fclose(fid);

end
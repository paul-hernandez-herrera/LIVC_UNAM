function SWC = readSWC(fName)
%function to read the swc file.
try
    %just in case that the file was saved as a dlm
    SWC=dlmread(fName);
catch  
    %opening the file for reading
    fidx=fopen(fName,'r'); 

    while ~feof(fidx)
        %reading each of the rows of the file
        line=fgetl(fidx); 

        %check that we have the correct format of the line
        if (isempty(line) || strncmp(line,'#',1))
            continue;
        end
        

        SWC = fscanf(fidx,'%f');
        filas = length(SWC)/7;
        SWC = reshape(SWC, [7,filas])';
        SWC = [strread(line,'%f',7)';SWC];
        
    end

    %close the file
    fclose(fidx);
    fclose('all');
end

end
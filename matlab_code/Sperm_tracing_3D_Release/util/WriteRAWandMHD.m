% Write a raw file and associated MHD.
% Format: WriteRAWandMHD(array, filePrefix,relpativePath)
% July. 
% Jan 2006. Support for relative paths
% November 16: Changed so that extension is removed automatically if
% present.
%
function WriteRAWandMHD(X, filePrefix,relpativePath,spacingOut)

    %Checks Spacing
    if (~exist('spacingOut','var'))
        spacingOut=[1 1 1];
    end     
    
    %just to remove the extension of the mhd file
    if length(filePrefix)>=3
        if strcmp(filePrefix(end-3:end),'.mhd')
            filePrefix(end-3:end) = [];
        end
    end
    
    mhdFile = [ filePrefix '.mhd' ];
    rawFile = [ filePrefix '.raw' ];
    
    elType = class(X);
    switch elType
        case 'int16'
            elTypeOut.mhd = 'MET_SHORT';
        case 'uint8'
            elTypeOut.mhd = 'MET_UCHAR';
            elTypeOut.vvi =  3;                        
        case 'uint16'
            elTypeOut.mhd = 'MET_USHORT';
            elTypeOut.vvi =  5;              
        case 'uint32'
            elTypeOut.mhd = 'MET_ULONG';
            elTypeOut.vvi =  9;                          
        case 'single'
            elTypeOut.mhd = 'MET_FLOAT';
            elTypeOut.vvi =  8;            
        case 'double'
            elTypeOut.mhd = 'MET_DOUBLE';
            elTypeOut.vvi =  8;      
        case 'logical'
            elTypeOut.mhd = 'MET_UCHAR';
            elTypeOut.vvi =  3;                                    
        otherwise
            outstr = sprintf('Data type unknown ("%s") - please modify WriteRAWandMHD.', elType);
            error(outstr);
    end
    % Open file in the destination
    % Relative path. Alberto Jan 2006
    if (exist('relpativePath','var'))
        mhdFileWithPath =  fullfile( relpativePath,mhdFile );        
        mhd = fopen(mhdFileWithPath, 'wt');                        
    else
        mhd = fopen(mhdFile, 'wt');            
    end   
    %Write mhd file
    fprintf(mhd, 'ObjectType = Image\n');
    fprintf(mhd, 'NDims = 3\n');
    fprintf(mhd, 'BinaryData = True\n');
    fprintf(mhd, 'BinaryDataByteOrderMSB = False\n');
    fprintf(mhd, 'ElementSpacing =  %g  %g   %g \n', spacingOut(1), spacingOut(2), spacingOut(3));    
    fprintf(mhd, 'DimSize = %d %d %d\n', size(X,1), size(X,2), size(X,3));
    fprintf(mhd, 'ElementType = %s\n', elTypeOut.mhd);
    fprintf(mhd, 'ElementDataFile = %s\n', rawFile);
    fclose(mhd);

    %Write raw file
    % Relative path. Alberto Jan 2006
    if (exist('relpativePath','var'))
        rawFileWithPath =  fullfile( relpativePath,rawFile );    
        raw = fopen(rawFileWithPath, 'wb');                        
    else
        raw = fopen(rawFile, 'wb');    
    end   
    fwrite(raw, X, class(X)); 
    fclose(raw);
%     clear all;
    
end

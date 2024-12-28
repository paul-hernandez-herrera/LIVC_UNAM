function [D, S]= compute_fast_marching(bMask, DistanceMap, start_points, end_points, length_,nb_iter_max, relPath, fNameOut_FastFront, FORCE_RECOMPUTE_FAST_FRONT, SPACING)
%function to compute the fast-marching
%fprintf('\nComputing fast-marching...');
if ( (~exist(fullfile(relPath,fNameOut_FastFront),'file')) || FORCE_RECOMPUTE_FAST_FRONT  )
    %computing fast-marching
%     D = perform_front_propagation_AS_FLOAT_BINARYCOUNT_3d(single(DistanceMap),...
%         single(start_points-1),single(end_points-1),nb_iter_max,bMask);
%       [D,S]= perform_front_propagation_double(double(DistanceMap),...
%         single(start_points-1),single(end_points-1),nb_iter_max,bMask);
       [D,S]= front_propagation_double_stopLength(double(DistanceMap),...
        single(start_points-1),single(end_points-1),nb_iter_max,bMask,length_); 
%        [D,S]= front_propagation_double_stopMicras(double(DistanceMap),...
%         single(start_points-1),single(end_points-1),nb_iter_max,bMask,length_); 
    %just to save the fast-marching
    indexFastFront =  D>10000; D(indexFastFront) = -0.01;
%     D2 = D; val_max =max(D2(:)); D2 = val_max-D2;D2(indexFastFront)=0;
    WriteRAWandMHD(D,fNameOut_FastFront,relPath,SPACING); 
    D(indexFastFront) = inf;
else
    %reading the fast-marching
    D=RAWfromMHD(fNameOut_FastFront,[],relPath);

    %giving infinity values to voxels not reached by fast-marching
    indexFastFront =  D == single(-0.01) ; 
    D(indexFastFront) = inf; 
end
%disp('Done');
end
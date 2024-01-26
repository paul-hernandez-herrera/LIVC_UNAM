from pathlib import Path
import numpy as np

def swc_to_vtk_lines(file_output, swc):
    swc = np.array(swc)
    
    points, conections = swc[:,2:5], swc[:,[0,6]]
    
    conections = conections[conections[:,1]>-1,:] -1
    conections = np.hstack((2*np.ones((conections.shape[0],1)),conections))

    file_output = Path(file_output)
    file_output = file_output if file_output.suffix == ".vtk" else file_output.with_suffix('.vtk')
    
    with open(file_output, 'w') as f:
        f.write('# vtk DataFile Version 2.0\n\nASCII\n\n')
        f.write('DATASET POLYDATA\n')
        f.write('POINTS {} float\n'.format(points.shape[0]))
        np.savetxt(f, points, fmt="%4.5f")
        f.write('LINES {:d} {:d}\n'.format(conections.shape[0],3*conections.shape[0]))
        np.savetxt(f, conections, fmt="%i")
    
def points_to_vectors(folder_path, file_name, positions, vectors):
    
    f = open(Path(folder_path) / (file_name + '.vtk'), 'w')
    f.write('# vtk DataFile Version 2.0\n\n')
    f.write('ASCII\n\n') 
    
    f.write('DATASET UNSTRUCTURED_GRID\n')
    f.write('POINTS {} float\n'.format(positions.shape[0]))
    np.savetxt(f, positions, fmt="%4.5f")
    
    f.write('POINT_DATA {}\n'.format(vectors.shape[0]))
    f.write('VECTORS vectors_direction float\n')
    np.savetxt(f, vectors, fmt="%4.5f")
    
    f.write('\nSCALARS colormap_ double\n')
    f.write('LOOKUP_TABLE default\n')
    np.savetxt(f,np.transpose( np.array(range(0,vectors.shape[0]))), fmt="%4.5f")
    
    f.close()
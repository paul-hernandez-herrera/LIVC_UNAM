from pathlib import Path
import numpy as np

def swc_to_vtk_lines(file_output, swc):
    swc = np.array(swc)

    # make sure nodes id start at zero
    I = swc[:,6] <= -1
    swc[:,[0,6]] =  swc[:,[0,6]]-np.min(swc[:,0])
    swc[I,1] = -1    
    
    points, conections = swc[:,2:5], swc[:,[0,6]]
    
    # elliminate nodes without connection
    conections =  np.delete(conections, np.where(conections[:,1] <= -1), axis = 0) 
    
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
    
def points_to_vectors(file_output, positions, vectors):
    file_output = Path(file_output)
    file_output = file_output if file_output.suffix == ".vtk" else file_output.with_suffix('.vtk')    
    with open(file_output, 'w') as f:
        f.write('# vtk DataFile Version 2.0\n\nASCII\n\n')
        f.write('DATASET UNSTRUCTURED_GRID\n')
        f.write('POINTS {} float\n'.format(positions.shape[0]))
        np.savetxt(f, positions, fmt="%4.5f")
        
        f.write('POINT_DATA {}\n'.format(vectors.shape[0]))
        f.write('VECTORS vectors_direction float\n')
        np.savetxt(f, vectors, fmt="%4.5f")
        
        f.write('\nSCALARS colormap_ double\nLOOKUP_TABLE default\n')
        np.savetxt(f, np.transpose(np.arange(vectors.shape[0])), fmt="%4.5f")
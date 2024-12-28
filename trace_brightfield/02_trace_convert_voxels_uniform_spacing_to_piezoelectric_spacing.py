import os
from pathlib import Path

# Cambiar el directorio de trabajo
workbookDir = Path(__file__).parent.parent.resolve()
os.chdir(workbookDir)
print(f"Currernt working directory: \n{os.getcwd()}")


from python_code.util import  util_swc, util_vtk
import numpy as np

# Define las carpetas con los datos originales
folder_uniform_spacing  = r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks\stacks_constant_sampling"
folder_piezo_spacing  = r"E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp2_stacks"
file_prefix  = r"Exp2_stacks" # Prefijo común de los archivos

# Crear carpeta de salida
folder_output = Path(folder_piezo_spacing, "trace_voxels")
folder_output.mkdir(parents=True, exist_ok=True)

for timepoint  in range(1,1000):
    # Construcción del nombre base de los archivos
    file_name = f"{file_prefix}_TP{timepoint:04}" # Formato: Exp16_stacks_TP0001, TP0002, etc.
    swc_file_name = f"{file_name}_DC_trace"  # Archivo SWC con reconstrucciones
    uniform_z_file_name = f"{file_name}_DC.txt"  # Archivo con posiciones Z uniformes
    piezo_z_file_name = f"{file_name}.txt"  # Archivo con posiciones Z del piezoeléctrico    
    
    trace_out_name = f"{file_name}_DC.swc" # Archivo de salida de la reconstruccion
    
    if Path(folder_uniform_spacing, swc_file_name+".swc").exists():
        # Lee el archivo SWC desde la carpeta de espaciamiento uniforme
        swc_data = util_swc.read_swc(folder_uniform_spacing, f"{swc_file_name}.swc")
        
        # Lee las posiciones Z uniformes desde un archivo de texto
        uniform_z_values = np.loadtxt( Path(folder_uniform_spacing, uniform_z_file_name) )        
        
        # Convert to microns: Asocia las posiciones Z de los nodos en el archivo SWC con las posiciones Z uniformes
        # Se utilizan los índices del archivo SWC para mapear.
        z_positions = uniform_z_values[swc_data[:, 4].astype(int)]
        
        # Lee las posiciones Z correspondientes al espaciamiento piezoeléctrico
        piezo_z_values = np.loadtxt(Path(folder_piezo_spacing, piezo_z_file_name) )
        
        # Encuentra el índice más cercano en las posiciones Z del piezoeléctrico
        idx = np.searchsorted(piezo_z_values, z_positions, side='left')  
        
        # Asegura que los índices estén dentro del rango válido
        idx = np.clip(idx, 0, len(piezo_z_values) - 2) 
        
        # Realiza una interpolación lineal (voxel position) entre las posiciones inferiores y superiores
        lower_bounds = piezo_z_values[idx]  # Limite inferior
        upper_bounds = piezo_z_values[idx + 1]  # Límite superior
        # Calcula las nuevas posiciones Z ajustadas al sistema piezoeléctrico
        new_z_positions = idx + (z_positions - lower_bounds) / (upper_bounds - lower_bounds)

        # Actualiza las posiciones Z en el archivo SWC con las nuevas coordenadas
        # Se suma 1 para ajustar al sistema de origen [1, 1, 1]
        swc_data[:, 4] = new_z_positions + 1
        
        # Guarda el archivo SWC actualizado en la carpeta de resultados
        output_swc_path = Path(folder_output, trace_out_name)
        util_swc.write_swc(output_swc_path, swc_data)
    
        # Prepara los datos para visualización en VTK (ajustando las coordenadas al origen [0, 0, 0])
        swc_data[:, 2:5] -= 1  # Ajuste de coordenadas
        util_vtk.swc_to_vtk_lines(output_swc_path, swc_data)

print("DONE\n")




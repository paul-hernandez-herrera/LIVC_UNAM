import numpy as np
import scipy.ndimage as ndi


def preprocess_3d_stack_for_AI_segmentation(V_raw):
    """
    Preprocesa un volumen 3D (stack) para segmentación de IA.
    - Aplica operaciones morfológicas para mejorar la calidad del stack.
    - Normaliza los valores del volumen en el rango [-1, 1].
    
    Parameters:
        V_raw: Volumen 3D para preprocesar
        
    Returns:
        numpy.ndarray: Volumen 3D procesado listo para segmentación.
    """  
    # Identificar voxeles con valor cero. Remover estos voxeles del preprocesamiento.
    # Estos voxels pueden corresponder a la corrección de drift
    zero_mask = V_raw == 0
    
    # Convertir el stack a tipo de datos de precisión simple
    V_raw = V_raw.astype(float)
    
    # Operación morfológica: apertura y cierre con un kernel 2D de 15x15x1
    kernel = np.ones((1, 15, 15), dtype = np.uint8)
    opened = ndi.grey_opening(V_raw, footprint=kernel)
    closed = ndi.grey_closing(opened, footprint=kernel)
    V_raw = V_raw - closed

    
    # Seleccionar solo los datos no cero
    data = V_raw[~zero_mask]
    
    # Calcular percentiles
    low_percentile = np.percentile(data, 0.1)   # Percentil 0.1
    high_percentile = np.percentile(data, 99.9) # Percentil 99.9
    
    # Limitar valores al rango de los percentiles
    data_clipped = np.clip(data, low_percentile, high_percentile)
    V_raw[~zero_mask] = data_clipped
    
    # Normalizar el stack 3D al rango [-1, 1] con media 0
    mean_val = np.mean(V_raw[~zero_mask])
    V_raw = V_raw - mean_val
    
    # Restaurar los píxeles con valor cero
    V_raw[zero_mask] = 0    

    # Escalar valores negativos al rango [-1, 0]
    neg_mask = V_raw < 0
    V_raw[neg_mask] /= np.abs(np.min(V_raw[neg_mask]))

    # Escalar valores positivos al rango [0, 1]
    pos_mask = V_raw > 0
    V_raw[pos_mask] /= abs(np.max(V_raw[pos_mask]))
    
    return V_raw

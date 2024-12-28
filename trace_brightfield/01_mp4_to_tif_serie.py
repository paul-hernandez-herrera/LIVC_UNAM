# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 09:00:43 2024

@author: paulh
"""

from pathlib import Path
import numpy as np
import imageio
import tifffile

# Este script procesa un archivo MP4 para generar una serie de imágenes en formato TIFF.
# Requisitos previos: Instalar FFmpeg para la funcionalidad de lectura de video.
# Variables de entrada:
# - folder_root: Ruta a la carpeta que contiene el archivo MP4.
# - file_mp4: Nombre del archivo MP4 a procesar.
# - file_out: Nombre de la carpeta de salida y prefijo de los archivos TIFF.

# Ruta de la carpeta que contiene el archivo MP4
folder_root = r'E:\SPERM\Fluorescencia_Campo_Claro\20241210 CC 4000fps Calceina y Fluo 4000fps - 90hz 20 micras'

# Nombre del archivo MP4 a procesar
file_mp4 = '20241210 Exp7.mp4'

# Prefijo para los archivos de salida y nombre de la carpeta de salida
file_out = 'Exp7'

# Crear carpeta de salida
folder_output = Path(folder_root, file_out)
folder_output.mkdir(parents=True, exist_ok=True)

# Cargar el archivo de video
mp4_path = Path(folder_root, file_mp4)
video = imageio.get_reader(mp4_path, 'ffmpeg')

# Contar el número total de fotogramas en el video
num_frames = video.count_frames()

# Procesar cada fotograma del video
for frame_idx in range(num_frames):
    # Leer el fotograma actual y extraer el canal de luminancia (escala de grises)
    frame = video.get_data(frame_idx)[:, :, 0]
    
    # Guardar el fotograma como un archivo TIFF
    output_path = folder_output / f"{file_out}_TP_{frame_idx:08}.tif"
    tifffile.imwrite(output_path, frame.astype(np.uint8))

print(f"Procesamiento completo. Imágenes guardadas en: {folder_output}")

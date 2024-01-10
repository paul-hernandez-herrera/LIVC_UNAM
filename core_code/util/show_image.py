import matplotlib.pyplot as plt
import numpy as np
from ..parameters_interface.ipwidget_basic import set_dropdown
from ipywidgets import widgets
from core_code.parameters_interface.ipwidget_basic import set_IntSlider, set_checkbox
from .util import imread
from pathlib import Path

########################################################################################################
########################################################################################################

def show_image_and_points(img, points, file_output = None):
    # Create figure with subplots for each image and its channels
    plt.close("all")
    plt.imshow(img, 'gray')
    plt.plot(points[:,0], points[:,1], linewidth=4)
    if file_output:
        plt.savefig(file_output)
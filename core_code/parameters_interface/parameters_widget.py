import ipywidgets as widgets
import torch
from IPython.display import display
from . import ipwidget_basic

    
################################################################################

class parameters_training_images():
    def __init__(self):
        print('------------------------------')
        print('\033[47m' '\033[1m' 'REQUIRED PARAMETERS' '\033[0m')
        print('------------------------------')
        self.folder_input_w = ipwidget_basic.set_text('Folder path input images:', 'Insert path here')   
        self.folder_target_w = ipwidget_basic.set_text('Folder path target mask:', 'Insert path here')
    
    def get(self):
        return {"folder_input"     : self.folder_input_w.value,
                "folder_target"    : self.folder_target_w.value}
    
################################################################################

class parameters_folder_path():
    def __init__(self):
        print('------------------------------')
        self.folder_path = ipwidget_basic.set_text('Folder or file path:', 'Insert path here')
        self.folder_output = ipwidget_basic.set_text('Folder output:', 'Insert path here')
        print('------------------------------')
    
    def get(self):
        return self.folder_path.value, self.folder_output.value

################################################################################

class parameters_create_training_set():
    def __init__(self):    
        print('------------------------------')
        print('\033[47m' '\033[1m' 'REQUIRED PARAMETERS' '\033[0m')
        print('------------------------------')
        self.folder_brightfield_w    = ipwidget_basic.set_text('Folder images - brightfield: ', 'Insert path here')
        self.folder_fluorescence_w   = ipwidget_basic.set_text('Folder images - fluorescence: ', 'Insert path here')
        self.folder_head_w           = ipwidget_basic.set_text('Folder target images - head: ', 'Insert path here')
        self.folder_flagellum_w      = ipwidget_basic.set_text('Folder target images - flagellum: ', 'Insert path here')
        self.folder_output_w         = ipwidget_basic.set_text('Folder output: ', 'Insert path here')
    
    def get(self):
        p = {"folder_brightfield"    : self.folder_brightfield_w.value,
             "folder_fluorescence"   : self.folder_fluorescence_w.value,
             "folder_head"           : self.folder_head_w.value,
             "folder_flagellum"      : self.folder_flagellum_w.value,
             "folder_output"         : self.folder_output_w.value}
        return p

################################################################################.

class parameters_device():
    def __init__(self):
        ##SETTING DEVICE
        device_options = [('CPU', 'cpu')]
        
        #checking if torch is available
        if torch.cuda.is_available():            
            for i in range(torch.cuda.device_count(),0,-1):
                device_options.insert(0, (torch.cuda.get_device_name(i-1), 'cuda:'+str(i-1)))
        
        #setting the option to get the device
        self.device_w = ipwidget_basic.set_dropdown('Device: ', device_options)
    
    def get_device(self):
        return self.device_w.value
    


          
class parameters_model_saving():
    def __init__(self):
        self.model_output_w = ipwidget_basic.set_text('Model output folder : ', 'Insert path here', show = False)
        self.model_checkpoint_w = ipwidget_basic.set_checkbox('Model checkpoint interval. ', False, show = False)
        
        self.model_checkpoint_frequency = ipwidget_basic.set_Int('Frequency', 10, show  = False)
        
        self.epoch_container = widgets.HBox(children= [self.model_checkpoint_w])
        self.main_container = widgets.VBox(children= [self.model_output_w, self.epoch_container])
        
        self.model_checkpoint_w.observe(self.handler_model_saving, names='value') 
        display(self.main_container)
        
    def handler_model_saving(self, change):
        if change.new:
            self.epoch_container.children = [self.model_checkpoint_w, self.model_checkpoint_frequency]
        else:
            self.epoch_container.children = [self.model_checkpoint_w]
            
    def get(self, str_id):
        if str_id == 'model_output_folder': return self.model_output_w.value         
        if str_id == 'model_checkpoint': return self.model_checkpoint_w.value
        if str_id == 'model_checkpoint_frequency': return self.model_checkpoint_frequency.value
        
################################################################################        
     

            
def set_parameters_construct_training_set_tubular_structure_from_swc(obj):
    print('------------------------------')
    print('\033[47m' '\033[1m' 'REQUIRED PARAMETERS' '\033[0m')
    print('------------------------------')

    folder_imgs_path_w = ipwidget_basic.set_text('Folder images path:', 'Insert path here')   
    #folder_swc_path_w = ipwidget_basic.set_text('Folder swc files path:', 'Insert path here')

    print('------------------------------')
    print('\033[47m' '\033[1m' 'OPTIONAL PARAMETERS' '\033[0m')
    print('------------------------------')
    
    folder_output_default = 'Default: "Folder images path"/training_set/'
    folder_output_path_w = ipwidget_basic.set_text('Folder output path:', folder_output_default)
    patch_size_img_w = ipwidget_basic.set_Int('Patch size (length x length): ', obj.patch_size_img)
    number_patches_w = ipwidget_basic.set_Int('# sub-images foreground: ', obj.number_patches)
    number_patches_random_w = ipwidget_basic.set_Int('# sub-images random pos: ', obj.number_patches)
    radius_tubular_mask_w = ipwidget_basic.set_Int('Radius tubular mask (GT): ', obj.radius_tubular_mask)
    draw_head_w = ipwidget_basic.set_checkbox('Draw head', obj.draw_head)
    percentile_w = ipwidget_basic.set_IntRangeSlider('Percentile normalization', obj.norm_perc_low, obj.norm_perc_high,0,100)



    parameters = {'folder_imgs_path_w' : folder_imgs_path_w,
                  #'folder_swc_path_w' : folder_swc_path_w,
                  'patch_size_img_w': patch_size_img_w,
                  'number_patches_w': number_patches_w,
                  'number_patches_random_w': number_patches_random_w,
                  'radius_tubular_mask_w': radius_tubular_mask_w,
                  'percentile_w': percentile_w,
                  'draw_head_w': draw_head_w,
                  'folder_output_path_w': folder_output_path_w,
                  'folder_output_default': folder_output_default}
    
    return parameters  
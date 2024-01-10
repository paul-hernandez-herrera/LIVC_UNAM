import torch, torchvision
from torch.nn import Conv2d
from torch import nn, tensor
from pathlib import Path
import numpy as np
from collections import OrderedDict
from .parameters_interface import ipwidget_basic
from .parameters_interface.parameters_widget import parameters_device
from .construct_training_set_Sperm_2d_Regression import preprocess_stack, crop_subvolumes_2D
from .util.util import imread, read_swc, write_csv, imwrite
from .util.show_image import show_image_and_points

class remove_head_from_trace:
    def __init__(self):
        #setting the parameters required to predict images
        # Set parameters required to predict images
        self.model_path_w = ipwidget_basic.set_text('Model path:', 'Insert path here')
        self.trace_path_w = ipwidget_basic.set_text('3D Trace path:', 'Insert path here')
        self.images_path_w = ipwidget_basic.set_text('3D Images path:', 'Insert path here')
        self.image_size_w = ipwidget_basic.set_Int('training image size (n x n):', 100)
        self.device_w = parameters_device()
        
    def run(self):
        device = self.device_w.get_device()
    
        # Predict images and return list of output file paths
        output = predict_neck_point_2D(self.trace_path_w.value, 
                                       self.images_path_w.value,
                                       self.image_size_w.value,
                                       self.model_path_w.value,
                                       device)
        
        return output
    
def predict_neck_point_2D(folder_traces, folder_images, train_img_size, model_path, device):

    folder_output = Path(folder_traces, "trace_head_removed")
    folder_output.mkdir(parents=True, exist_ok=True)

    model = load_model(model_path = model_path, device = device)
    model.eval()

    traces_paths = [Path(p) for p in Path(folder_traces).iterdir() if p.suffix in {".swc"}]
    if not traces_paths:
        raise Exception(f"{folder_traces} does not have any trace (*.swc file).")
    with torch.no_grad():
        for trace_p in traces_paths:
            img3D, swc = get_image_for_trace(trace_p, folder_images), read_swc(trace_p.parent, trace_p.name)

            img2D = preprocess_stack(img3D)

            # get left upper corner of image to be used to predict neck point
            left_upper_corner = np.array([[swc[0,3], swc[0,2]]]) - (train_img_size//2)

            # crop image and update the left upper corner position
            img_cropped, left_upper_corner = crop_subvolumes_2D(img2D, left_upper_corner, train_img_size)

            # change image to tensor, float and format [B, C, W, H] = [1, 1, W, H]
            img = tensor(img_cropped.astype(np.float32)).float().unsqueeze(0).unsqueeze(0).to(device= device, dtype = torch.float32)

            # network output and convert to numpy
            network_output = model(img).cpu().numpy()

            # convert neck_point to the input image (img2D) coordinates
            neck_point_pos = left_upper_corner + network_output[0,0,::-1]

            swc = swc_remove_head(swc, neck_point_pos)
            file_name_base = get_file_name_from_trace(trace_p)
            write_csv(Path(folder_output,  f"{file_name_base}_raw.swc"), swc)

            #just to display the head_removed trace
            trace = swc[:,2:4]-left_upper_corner[:,::-1]
            I = (trace[:,0]<0) | (trace[:,0]>=train_img_size-1) | (trace[:,1]<0) | (trace[:,1]>=train_img_size-1)
            trace = trace[~I,:]
            show_image_and_points(img_cropped,trace, Path(folder_output, f"{file_name_base}.png"))

            


def swc_remove_head(swc, neck_point_pos):
    # compute distance from neck point to all points in trace 
    distances = np.sqrt((swc[:,3]-neck_point_pos[0,0])**2 + (swc[:,2]-neck_point_pos[0,1])**2 )
    ind = np.argmin(distances)

    # remove points corresponding to head
    swc = swc[ind::,:]

    # correct id and parents from swc
    label = np.arange(swc.shape[0])
    swc[:,0] = label
    swc[:,6] = label-1
    swc[0,6] = -1

    return swc
    

def get_image_for_trace(trace_path, folder_images):
    file_name = Path(trace_path).stem

    for num_digits in [3, 4]:
        for ID in {"_DC", ""}:
            n1, n2 = file_name.find("_TP"), file_name.find(ID+"_LogN_rec_FM")
            file_ID, num_stack = file_name[0:n1], file_name[n1+3:n2]
            if num_stack.isdigit():
                num_stack = int(num_stack)
                image_file_name = f"{file_ID}_TP{num_stack:0{num_digits}}{ID}"
                for file_ext in {".mhd", ".tif"}:
                    image_path = Path(folder_images, image_file_name + file_ext)
                    if image_path.is_file():
                        return imread(image_path)
    raise Exception(f"{trace_path} does not have any associated image.")

def get_file_name_from_trace(trace_path):
    file_name = Path(trace_path).stem

    for _ in [3, 4]:
        for ID in {"_DC", ""}:
            n1, n2 = file_name.find("_TP"), file_name.find(ID+"_LogN_rec_FM")
            file_ID, num_stack = file_name[0:n1], file_name[n1+3:n2]
            if num_stack.isdigit():
                num_stack = int(num_stack)
                return f"{file_ID}_TP{num_stack:04}"
    

def load_model(model_path, device = 'cpu'):
    state_dict = torch.load(model_path, map_location= device)

    n_channels_input = state_dict[list(state_dict.keys())[0]].size(1)
    output_nodes = state_dict[list(state_dict.keys())[-1]].size(0)

    # We assume that current model is developed for 2D data
    n_rows = int(output_nodes/2)
    n_columns = 2
    
    model = get_model('resnet50', n_channels_input, np.array([n_rows, n_columns])).to(device= device)
    
    try:
        model.load_state_dict(state_dict)
    except:
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            
            name = k[10:] # remove `module.`
            new_state_dict[name] = v
        # load params
        model.load_state_dict(new_state_dict)
    
    return model

def get_model(model_type, n_channels_input, output_shape):
    if model_type == 'resnet50':
        model = torchvision.models.resnet101()
        
        # Adjust the conv1 to the number of input channels
        model.conv1 = Conv2d(n_channels_input, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        
        # convert shape to single vector output
        output_nodes = output_shape[0]*output_shape[1]
        
        # Adjust the fc to the number of output classes
        model.fc = nn.Sequential(
            nn.Linear(in_features=2048, 
                                out_features= output_nodes
                                ),
            nn.Unflatten(1, torch.Size([int(output_shape[0]), int(output_shape[1])]))
        )

        return model 

def manually_remove_head(trace_p, folder_images, folder_output, ind):
    img_size = 128

    img3D, swc = get_image_for_trace(trace_p, folder_images), read_swc(trace_p.parent, trace_p.name)
    img2D = preprocess_stack(img3D)

    # get left upper corner of image to be used to predict neck point
    left_upper_corner = np.array([[swc[0,3], swc[0,2]]]) - (img_size//2)

    # crop image and update the left upper corner position
    img_cropped, left_upper_corner = crop_subvolumes_2D(img2D, left_upper_corner, img_size)

    # remove points corresponding to head
    swc = swc[ind::,:]

    # correct id and parents from swc
    label = np.arange(swc.shape[0])
    swc[:,0] = label
    swc[:,6] = label-1
    swc[0,6] = -1

    file_name_base = get_file_name_from_trace(trace_p)
    write_csv(Path(folder_output,  f"{file_name_base}_raw.swc"), swc)

    #just to display the head_removed trace
    trace = swc[:,2:4]-left_upper_corner[:,::-1]
    I = (trace[:,0]<0) | (trace[:,0]>=img_size-1) | (trace[:,1]<0) | (trace[:,1]>=img_size-1)
    trace = trace[~I,:]
    show_image_and_points(img_cropped,trace, Path(folder_output, f"{file_name_base}.png"))

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 11:31:28 2024

@author: paulh
"""
from torch import tensor, cat
from torch.nn import Conv3d, Sequential, BatchNorm3d, ReLU, MaxPool3d, ConvTranspose3d, Module
from torch.nn import functional

class UNet_3D(Module):
    def __init__(self):
        super().__init__()
        scale = 2
        # BLOQUE 1
        self.block1 = Sequential(
            Conv3d(in_channels = 1, out_channels = 64//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 64//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 64//scale, out_channels = 64//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 64//scale),
            ReLU(inplace=True)            
            )
        self.maxpool1 = MaxPool3d(kernel_size = (2,2,2))

        # BLOQUE 2
        self.block2 = Sequential(
            Conv3d(in_channels = 64//scale, out_channels = 128//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 128//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 128//scale, out_channels = 128//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 128//scale),
            ReLU(inplace=True)            
            )
        self.maxpool2 = MaxPool3d(kernel_size = (2,2,2))

        # BLOQUE 3
        self.block3 = Sequential(
            Conv3d(in_channels = 128//scale, out_channels = 256//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 256//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 256//scale, out_channels = 256//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 256//scale),
            ReLU(inplace=True)            
            )
        self.maxpool3 = MaxPool3d(kernel_size = (1,2,2))
        
        # BLOQUE 4
        self.block4 = Sequential(
            Conv3d(in_channels = 256//scale, out_channels = 512//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 512//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 512//scale, out_channels = 512//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 512//scale),
            ReLU(inplace=True)            
            )
        self.maxpool4 = MaxPool3d(kernel_size = (1,2,2))
        
        # BLOQUE 5
        self.bottom = Sequential(
            Conv3d(in_channels = 512//scale, out_channels = 1024//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 1024//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 1024//scale, out_channels = 1024//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 1024//scale),
            ReLU(inplace=True)            
            )
        
        
        self.up4 = ConvTranspose3d(in_channels = 1024//scale, out_channels = 512//scale, kernel_size=(1,2,2), stride = (1,2,2))

        # BLOQUE UP 1
        self.block_up4 = Sequential(
            Conv3d(in_channels = 1024//scale, out_channels = 512//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 512//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 512//scale, out_channels = 512//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 512//scale),
            ReLU(inplace=True)            
            )     

        self.up3 = ConvTranspose3d(in_channels = 512//scale, out_channels = 256//scale, kernel_size=(1,2,2), stride = (1,2,2))
        
        # BLOQUE UP 2
        self.block_up3 = Sequential(
            Conv3d(in_channels = 512//scale, out_channels = 256//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 256//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 256//scale, out_channels = 256//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 256//scale),
            ReLU(inplace=True)            
            )
        
        self.up2 = ConvTranspose3d(in_channels = 256//scale, out_channels = 128//scale, kernel_size=(2,2,2), stride = (2,2,2))        
        # BLOQUE UP 3
        self.block_up2 = Sequential(
            Conv3d(in_channels = 256//scale, out_channels = 128//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 128//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 128//scale, out_channels = 128//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 128//scale),
            ReLU(inplace=True)            
            )
        
        self.up1 = ConvTranspose3d(in_channels = 128//scale, out_channels = 64//scale, kernel_size=(2,2,2), stride = (2,2,2))
        
        # BLOQUE FINAL
        self.block_up1 = Sequential(
            Conv3d(in_channels = 128//scale, out_channels = 64//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 64//scale),
            ReLU(inplace=True),
            Conv3d(in_channels = 64//scale, out_channels = 64//scale, kernel_size=(3,3,3), padding = 1),
            BatchNorm3d(num_features = 64//scale),
            ReLU(inplace=True),
            )    
        
        self.conv_final = Conv3d(in_channels = 64//scale, out_channels = 1, kernel_size=(3,3,3), padding = 1)

    def forward(self, x):
        # bloque 1
        x_1 = self.block1(x)
        x = self.maxpool1(x_1)
        
        #bloque 2
        x_2 = self.block2(x)
        x = self.maxpool2(x_2)
    
        #bloque 3
        x_3 = self.block3(x)
        x = self.maxpool3(x_3)
        
        #bloque 4
        x_4 = self.block4(x)
        x = self.maxpool4(x_4)

        # bloque ultimo
        x = self.bottom(x)

        x_up4 = self.up4(x)

        # bloque up1
        x = self.concatenate(x_4, x_up4)
        x = self.block_up4(x)

        # UP 1
        x_up3 = self.up3(x)
        x = self.concatenate(x_3, x_up3 )
        x = self.block_up3(x)

        # UP 2
        x_up2 = self.up2(x)
        x = self.concatenate(x_2, x_up2)
        x = self.block_up2(x)
        
        # UP 3
        x_up1 = self.up1(x)
        x = self.concatenate(x_1, x_up1)
        x = self.block_up1(x)
        
        #Final
        output = self.conv_final(x)
        
        return output

    def concatenate(self, x1, x2):
        # Assuming x1 and x2 have shape (B, C, D, H, W)
        # x1 comes from the decoder and x2 is the tensor upsampled in the decoder
        
        diff_size = tensor(x1.shape[2:]) - tensor(x2.shape[2:])
        half_pad_size = diff_size//2
        
        m = functional.pad(x2, (half_pad_size[2], diff_size[2]-half_pad_size[2], 
                       half_pad_size[1], diff_size[1]-half_pad_size[1],
                       half_pad_size[0], diff_size[0]-half_pad_size[0]), mode='reflect')
        
        return cat((x1,m),dim=1)
# with help from https://github.com/usuyama/pytorch-unet/blob/master/pytorch_unet.py
import torch
import torch.nn as nn

def double_conv(in_channels, out_channels):
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, 3, padding=1),
        nn.ReLU(inplace=True),
        nn.Conv2d(out_channels, out_channels, 3, padding=1),
        nn.ReLU(inplace=True)
    )   


class CArrNet(nn.Module):

    def __init__(self, n_inputs = 1,sigmoid = False):
        super().__init__()
                
        self.dconv_down1 = double_conv(n_inputs, 4)
        self.dconv_down2 = double_conv(4, 16)
        self.dconv_down3 = double_conv(16, 32)
        self.dconv_down4 = double_conv(32, 1)        

        self.maxpool = nn.MaxPool2d(2)

        
        self.conv_last = nn.Linear(in_features=2,out_features=10,bias = True)

        self.sigmoid = sigmoid
        self.sigmoid_layer = nn.Sigmoid()
        
        
    def forward(self, x):
        conv1 = self.dconv_down1(x)
        x = self.maxpool(conv1)

        #print(x.shape)

        conv2 = self.dconv_down2(x)
        x = self.maxpool(conv2)
        
        #print(x.shape)
        
        conv3 = self.dconv_down3(x)
        x = self.maxpool(conv3)   
        
        #print(x.shape)
        
        conv4 = self.dconv_down4(x)
        x = self.maxpool(conv4)
        x = self.maxpool(x)
        x = self.maxpool(x)
        x = self.maxpool(x)
        x = self.maxpool(x)
        
        
        
        #print(x.shape)
        
        out = self.conv_last(x)
        
        if self.sigmoid:
            out = self.sigmoid_layer(out)

        return [out]
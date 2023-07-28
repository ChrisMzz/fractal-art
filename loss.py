import torch
from torch.autograd import Variable
import fractalize as frctl
import utility
import matplotlib.pyplot as plt
import pdb
SMOOTH = 1e-10

# image to image loss
def dice_loss(source,target):
    loss = -2*(torch.sum(source*target) + SMOOTH)/(torch.sum(source**2) + torch.sum(target**2) + 2*SMOOTH)
    return(loss)


def frctl_loss(source, target):
    source_fcts, target_fcts = [], []
    for fct in source:
        img = frctl.julia_from_2Darray(fct.detach().numpy())
        img = utility.set_nan_to_zero(img)
        img = torch.from_numpy(img)
        source_fcts.append(torch.unsqueeze(img, dim=0))
    for fct in target:
        img = frctl.julia_from_2Darray(fct.detach().numpy())
        img = utility.set_nan_to_zero(img)
        img = torch.from_numpy(img)
        target_fcts.append(torch.unsqueeze(img, dim=0))
    source_fcts, target_fcts = torch.cat(source_fcts), torch.cat(target_fcts)
    
    source_fcts = Variable(source_fcts.data, requires_grad=True)
    target_fcts = Variable(target_fcts.data, requires_grad=True)
    #pdb.set_trace()
    return dice_loss(source_fcts, target_fcts)
    
    

import torch
SMOOTH = 1e-10

def dice_loss(source,target):
    loss = -2*(torch.sum(source*target) + SMOOTH)/(torch.sum(source**2) + torch.sum(target**2) + 2*SMOOTH)
    return(loss)
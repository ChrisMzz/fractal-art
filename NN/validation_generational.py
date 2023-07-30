import sys
sys.path.insert(0, '.')
import os
import torch
import tqdm
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import fractalize as frctl
import utility
import pdb


DATA_NAME = "test"
EXPCE_NAME = "test1000"

MODEL_FOLDER = fr'EXPCE\{EXPCE_NAME}\model'
MODEL_NUMBER = 200

TO_VALIDATE_FOLDER = fr'DATA\{DATA_NAME}\validation_data\images'
VALIDATED_FOLDER = fr'EXPCE\{EXPCE_NAME}\validated\model{MODEL_NUMBER}'
for folder in [VALIDATED_FOLDER, fr'{VALIDATED_FOLDER}\functions', fr'{VALIDATED_FOLDER}\cheat_sheets']:
    os.makedirs(folder,exist_ok=True)

model = torch.load(MODEL_FOLDER + f"/model{MODEL_NUMBER}.pth")

fnames = os.listdir(TO_VALIDATE_FOLDER)
for i in tqdm.trange(len(fnames)):
    f = fnames[i]
    img = io.imread(fr'{TO_VALIDATE_FOLDER}\{f}')
    img = np.reshape(img,(1,) + img.shape)
    #img = img[0]
    img = torch.from_numpy(img)
    img = img.float()
    #img = img/img.max()
    func = model(img)[0][0]
    func = func.detach().numpy()
    pred = frctl.julia_from_2Darray(func)
    pred = utility.set_nan_to_zero(pred)   
    io.imsave(fr'{VALIDATED_FOLDER}\cheat_sheets\{f}',pred)
    np.save(fr'{VALIDATED_FOLDER}\functions\{f[:-4]}.npy', func)
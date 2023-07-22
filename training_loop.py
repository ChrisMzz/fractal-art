import os
import numpy as np
import loss
import unet_variation as unet
import fractalize as frctl
import torch
import torch.nn as nn
import tqdm
import matplotlib.pyplot as plt
import utility
import generator

#Defining parameters
DATA_NAME = "test"
EXPCE_NAME = "test"


SOURCE_IMAGE_FOLDER = fr'DATA/{DATA_NAME}/training_data/images'
SOURCE_FUNCTION_FOLDER = fr'DATA/{DATA_NAME}/training_data/functions'

PRED_FOLDER = fr'EXPCE/testexpce.png'

MODEL_FOLDER = fr'EXPCE/{EXPCE_NAME}/model'
for folder in [MODEL_FOLDER]:
    os.makedirs(folder, exist_ok=True)


inputs, targets = os.listdir(SOURCE_IMAGE_FOLDER), os.listdir(SOURCE_FUNCTION_FOLDER)
inputs, targets = [fr'{SOURCE_IMAGE_FOLDER}/{f}' for f in inputs], [fr'{SOURCE_FUNCTION_FOLDER}/{f}' for f in targets]

BATCH_SIZE = 5
NUM_STEPS = 1000 # switched back to 2000 to test data augmentation using voodoo magic i guess
LEARNING_RATE = 0.00005

#PATCH_SIZE = (512,512)

SKELETON = False
CONTOUR = False
RESCALE = 1

gene = generator.Generator(inputs, targets, batch_size=BATCH_SIZE)

#load model
model = unet.UNet().float()

#load optimizer
optimizer = torch.optim.Adam(model.parameters(), lr = LEARNING_RATE)

#Training loop
loss_plot = np.zeros(NUM_STEPS)
p_bar = tqdm.trange(NUM_STEPS)
for i in p_bar:
    optimizer.zero_grad()
    #next batch
    x, y = next(gene)
    x = x.float()
    y = y.float()
    

    #output of the net
    y_pred = model(x)[0]

    l = loss.dice_loss(y_pred,y)

    l.backward()
    optimizer.step()
    loss_plot[i] = l.detach().cpu().numpy()
    #p_bar.set_postfix({'loss': np.mean(loss_plot[max(0,i-50):i+1])})

    if i%500 == 0 and i > 0:
        plt.plot(loss_plot)
        plt.plot(utility.running_mean(loss_plot,50))
        plt.savefig(os.path.join(MODEL_FOLDER,'loss_function.svg'))
        plt.close()


#Save model
torch.save(model,os.path.join(MODEL_FOLDER,'model.pth'))

#save loss
plt.plot(loss_plot)
plt.plot(utility.running_mean(loss_plot,50))
plt.savefig(os.path.join(MODEL_FOLDER,'loss_function.svg'))

"""
#predict images
model.eval()
fnames = os.listdir(TO_PREDICT_FOLDER)
for i in tqdm.trange(len(fnames)):
    f = fnames[i]
    img = io.imread(os.path.join(TO_PREDICT_FOLDER,f))
    img = np.reshape(img,(1,) + img.shape)
    img = torch.from_numpy(img/255.0)
    #img = img/img.max()
    pred = pf.predict(model,img,patch_size = PATCH_SIZE,margin = (128,128))[0][0,0].detach().cpu().numpy()
    io.imsave(os.path.join(PREDICTED_FOLDER,f),pred)

"""









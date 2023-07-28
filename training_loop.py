import os
import numpy as np
import loss
import carrnet
import fractalize as frctl
import torch
import torch.nn as nn
import tqdm
import matplotlib.pyplot as plt
import utility
import generator
import pdb

#Defining parameters
DATA_NAME = "test"
EXPCE_NAME = "test1000"


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

gene = generator.Generator(inputs, targets, batch_size=BATCH_SIZE).gene()

#load model
model = carrnet.CArrNet().float()

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

    # print(x.shape, y.shape)

    #output of the net
    y_pred = model(x)[0]

    # squeeze
    y_pred, y = torch.squeeze(y_pred, dim=1), torch.squeeze(y, dim=1)
    
    l = loss.frctl_loss(y_pred,y)

    #pdb.set_trace()

    l.backward()
    optimizer.step()
    loss_plot[i] = l.detach().cpu().numpy()
    p_bar.set_postfix({'loss': np.mean(loss_plot[max(0,i-50):i+1])})

    if i%50 == 0 and i > 0:
        plt.plot(loss_plot)
        plt.plot(utility.running_mean(loss_plot,50))
        plt.savefig(os.path.join(MODEL_FOLDER,'loss_function.svg'))
        plt.close()
        
    if i%200 == 0 and i > 0:
        torch.save(model,os.path.join(MODEL_FOLDER,f'model_{i}.pth'))


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









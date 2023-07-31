import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../lib')
import fractalize as frctl
import utility
import os
import tqdm
from skimage.io import imsave

# will use this to generate data

# I'll try and make this as "automatic" as possible, with minimal user input needed.
# This implies :
#   - evaluating images' relevance by image diversity
#   - randomizing series expansions efficiently
#   - avoiding trivial cases (near the null function for example)

show = False

AMOUNT = 50
training, validation = int(AMOUNT*0.8), int(AMOUNT*0.2) # 80-20 rule for training and validation data

DATA_NAME = 'test'
PATH_TO_SAVE = fr'NN/DATA/{DATA_NAME}'
for folder in [PATH_TO_SAVE, fr'{PATH_TO_SAVE}/training_data', fr'{PATH_TO_SAVE}/validation_data', \
            fr'{PATH_TO_SAVE}/training_data/functions', fr'{PATH_TO_SAVE}/training_data/images', \
            fr'{PATH_TO_SAVE}/validation_data/functions', fr'{PATH_TO_SAVE}/validation_data/images', \
            fr'{PATH_TO_SAVE}/training_data/cheat_sheets', fr'{PATH_TO_SAVE}/validation_data/cheat_sheets']:
    os.makedirs(folder, exist_ok=True)

training_bar = tqdm.trange(training)
for fname in training_bar:
    tries = 1
    arr = 1-2*np.random.rand(2,10)
    cheat = frctl.julia_from_array(arr)
    image = utility.regularize(cheat)
    num_valid = np.sum(image>0)
    # np.isnan(image).all() 
    # this outputs True if all values are NaN. equivalent to num_valid < 1
    training_bar.set_postfix({'tries':tries, 'num_valid':num_valid})
    while num_valid < 4096:
        tries += 1
        arr = 1-2*np.random.rand(2,10)
        cheat = frctl.julia_from_array(arr)
        image = utility.regularize(cheat)
        num_valid = np.sum(image>0)
        training_bar.set_postfix({'tries':tries, 'num_valid':num_valid})
    if show:
        fig, (ax1, ax2) = plt.subplots(1,2)
        ax1.imshow(cheat)
        ax2.imshow(image)
        plt.show()
    imsave(fr'{PATH_TO_SAVE}/training_data/cheat_sheets/{fname}.jpg', np.array(cheat*255,dtype=np.uint8), check_contrast=False)
    imsave(fr'{PATH_TO_SAVE}/training_data/images/{fname}.jpg', np.array(image*255,dtype=np.uint8), check_contrast=False)
    np.save(fr'{PATH_TO_SAVE}/training_data/functions/{fname}.npy', arr)

validation_bar = tqdm.trange(training, training+validation)
for fname in validation_bar:
    tries = 1
    arr = 1-2*np.random.rand(2,10)
    cheat = frctl.julia_from_array(arr)
    image = utility.regularize(cheat)
    num_valid = np.sum(image>0)
    validation_bar.set_postfix({'tries':tries, 'num_valid':num_valid})
    while num_valid < 4096:
        tries += 1
        arr = 1-2*np.random.rand(2,10)
        cheat = frctl.julia_from_array(arr)
        image = utility.regularize(cheat)
        num_valid = np.sum(image>0)
        validation_bar.set_postfix({'tries':tries, 'num_valid':num_valid})
    if show:
        fig, (ax1, ax2) = plt.subplots(1,2)
        ax1.imshow(cheat)
        ax2.imshow(image)
        plt.show()
    imsave(fr'{PATH_TO_SAVE}/validation_data/cheat_sheets/{fname}.jpg', np.array(cheat*255,dtype=np.uint8), check_contrast=False)
    imsave(fr'{PATH_TO_SAVE}/validation_data/images/{fname}.jpg', np.array(image*255,dtype=np.uint8), check_contrast=False)
    np.save(fr'{PATH_TO_SAVE}/validation_data/functions/{fname}.npy', arr)








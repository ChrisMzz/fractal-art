from skimage.io import imread
import numpy as np
import torch


class Generator():
    def __init__(self, inputs, targets, batch_size=1):
        
        self.list_data = []
        self.batch_size = batch_size
        
        for f,g in zip(inputs,targets):
            x,y = (imread(f),np.load(g))
            
            self.list_data.append((torch.from_numpy(x),torch.from_numpy(y)))

    def gene(self):
        
        while True:
            idx = np.random.randint(len(self.list_data),size = self.batch_size)
            temp_batch = []
            for i in idx:
                x,y = self.list_data[i]
                combined = torch.cat([x,y])
                temp_batch.append(combined)
            img_batch, fct_batch = temp_batch[:,0], temp_batch[:,1]
            yield img_batch, fct_batch


if __name__ == '__main__':
    import os
    import matplotlib.pyplot as plt
    
    DATA_NAME = "test"
    
    SOURCE_IMAGE_FOLDER = fr'DATA/{DATA_NAME}/training_data/images'
    SOURCE_FUNCTION_FOLDER = fr'DATA/{DATA_NAME}/training_data/functions'

    #loading data
    inputs, targets = os.listdir(SOURCE_IMAGE_FOLDER), os.listdir(SOURCE_FUNCTION_FOLDER)
    inputs, targets = [fr'{SOURCE_IMAGE_FOLDER}/{f}' for f in inputs], [fr'{SOURCE_FUNCTION_FOLDER}/{f}' for f in targets]

    gene = Generator(inputs, targets, batch_size=5).gene()

    x,y = next(gene)

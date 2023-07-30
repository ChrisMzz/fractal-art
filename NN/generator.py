from skimage.io import imread
import numpy as np
import torch


class Generator():
    def __init__(self, inputs, targets, batch_size=1):
        
        self.list_data = []
        self.batch_size = batch_size
        
        for f,g in zip(inputs,targets):
            x,y = (imread(f)>0,np.load(g))
            
            self.list_data.append((torch.from_numpy(x),torch.from_numpy(y)))

    def gene(self):
        
        while True:
            idx = np.random.randint(len(self.list_data),size = self.batch_size)
            img_batch, fct_batch = [], []
            for i in idx:
                x,y = self.list_data[i]
                img = torch.unsqueeze(x, dim=0)
                fct = torch.unsqueeze(y, dim=0)
                img_batch.append(torch.unsqueeze(img, dim=0))
                fct_batch.append(torch.unsqueeze(fct, dim=0))
            
            
            yield torch.cat(img_batch), torch.cat(fct_batch)


if __name__ == '__main__':
    import os
    import matplotlib.pyplot as plt
    import fractalize as frctl
    import utility
    
    DATA_NAME = "test"
    
    SOURCE_IMAGE_FOLDER = fr'DATA/{DATA_NAME}/training_data/images'
    SOURCE_FUNCTION_FOLDER = fr'DATA/{DATA_NAME}/training_data/functions'

    #loading data
    inputs, targets = os.listdir(SOURCE_IMAGE_FOLDER), os.listdir(SOURCE_FUNCTION_FOLDER)
    inputs, targets = [fr'{SOURCE_IMAGE_FOLDER}/{f}' for f in inputs], [fr'{SOURCE_FUNCTION_FOLDER}/{f}' for f in targets]

    gene = Generator(inputs, targets, batch_size=5).gene()

    x,y = next(gene)

    fig, (ax1, ax2) = plt.subplots(1,2)
    
    print(x.shape,y.shape)
    
    img = np.transpose(x[0], (1,2,0))
    fct = np.transpose(y[0], (1,2,0))
    ax1.imshow(img)
    fractal = frctl.julia_from_array(fct)
    fractal = utility.set_nan_to_zero(fractal)
    ax2.imshow(fractal)
    plt.show()
    

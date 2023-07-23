import numpy as np
from skimage import filters, morphology




# FROM https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def formatter():
    pass


def set_nan_to_zero(image):
    image[np.isnan(image)] = 0
    return image

def regularize(image):
    im = image
    im = set_nan_to_zero(im)
    im = im*morphology.remove_small_objects(im>0, 64)
    im = filters.gaussian(im, 3)
    im = im*(im > 0.15)
    return im



if __name__ == '__main__':
    from skimage import io
    import matplotlib.pyplot as plt
    import fractalize as frctl


    PATH_TO_FUNCTION = fr'C:\Users\33783\OneDrive\Bureau\000Chris\Scolarité\Random Scripts\Python Scripts\fractal-art\DATA\data_gen_test\training_data\functions\0.npy'

    fig, (ax1, ax2) = plt.subplots(1,2)

    image = frctl.julia_from_array(np.load(PATH_TO_FUNCTION))
    
    reg = regularize(image)
    ax1.imshow(image)
    ax2.imshow(reg)
    
    plt.show()
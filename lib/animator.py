import fractalize as frctl
import numpy as np


def random_function_array(order):
    return np.array([1-2*np.random.rand(order), 1-2*np.random.rand(order)])


def lerp(arr1, arr2, size):
    return [arr1*(1-t) + arr2*t for t in np.linspace(0,1,size)]
    
def lerp_projector(space1, space2, size):
    if space1.shape != space2.shape:
        return
    if len(space1.shape) == 2:
        return np.array(lerp(space1, space2, size))
    space = []
    for a in range(len(space1)):
        arr1 = space1[a]
        arr2 = space2[a]
        space.append(lerp_projector(arr1, arr2, size))
    return np.array(space)


def fill(arr_list, new_resolution, ordertxt, progress_bar):
    dims = arr_list.shape[:-2]
    hyperplane = []
    if len(dims) > 1:
        for dim in range(dims[0]):
            hyperplane.append(fill(arr_list[dim,], new_resolution, ordertxt, progress_bar))
    else:
        for arr in arr_list:
            progress_bar.update(1)
            img = frctl.julia_from_2Darray(arr, (new_resolution,new_resolution), frctl.parametric_cmap)
            img = colorswap(img, ordertxt)
            img = (255*img).astype(np.uint8)
            hyperplane.append(img)
    return np.array(hyperplane)


def colorswap(img, ordertxt): # img shape is (h,w,3)
    r, g, b = img.transpose(2,0,1)
    img = []
    for char in ordertxt:
        if char == 'r':
            img.append(r)
        if char == 'g':
            img.append(g)
        if char == 'b':
            img.append(b)
        if len(img) >= 3:
            break
    img = np.array(img)
    return img.transpose(1,2,0)


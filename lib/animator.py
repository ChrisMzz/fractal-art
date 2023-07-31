import fractalize as frctl
import utility as util
import numpy as np
from skimage import io
import tqdm
from PIL import Image

def random_function_array(order):
    return np.array([1-2*np.random.rand(order), 1-2*np.random.rand(order)])


def lerp(arr1, arr2, size):
    return [arr1*(1-t) + arr2*t for t in np.linspace(0,1,size)]
    

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


if __name__ == '__main__':
    import os
    
    gif = []

    arr1, arr2, arr3 = random_function_array(11), random_function_array(11), random_function_array(11)
    
    anim = lerp(arr1, arr2, 50) + lerp(arr2, arr3, 50) + lerp(arr3, arr1, 50)
    
    anim_name = 'fourth_test_lerp'

    os.makedirs(f'dump/{anim_name}', exist_ok=True)
    
    for frame in tqdm.trange(len(anim)):
        arr = anim[frame]
        frctl.set_thresh(50)
        img = frctl.julia_from_2Darray(arr, (1024,1024), frctl.bernstein)
        io.imsave(f'dump/{anim_name}/{frame}.png', img)
        img = Image.fromarray((255*img).astype(np.uint8))
        gif.append(img)
    
    
    gif[0].save(f'dump/{anim_name}.gif', save_all=True, optimize=False, append_images=gif[1:], loop=0)


import napari
from napari.layers import Image # for magicgui and selection error handling
from napari.utils import progress
import tqdm
from qtpy.QtWidgets import QPushButton
from magicgui import magicgui
import pathlib # to include paths in magicgui widgets
from PIL import Image as pilimage

import sys
sys.path.insert(0, '../lib')
import animator as anim
import fractalize as frctl
import utility as util
import numpy as np
import os
from skimage import io
import random

frctl.set_thresh(50)
RESOLUTION = 256
SAVE_LOCATION = 'dump/browser'
ORDER = 11

def func_gen():
    while True: # I'm so sorry
        yield anim.random_function_array(ORDER)

gene = func_gen()

def debug_reload():
    viewer.add_image(np.zeros((2,2)))
    del viewer.layers[-1]


def viewer_next():
    arr = next(gene)
    img = frctl.julia_from_2Darray(arr, (RESOLUTION,RESOLUTION), frctl.bernstein)
    ordertxt = list('rgb')
    random.shuffle(ordertxt)
    ordertxt = ''.join(ordertxt)
    img = anim.colorswap(img, ordertxt)
    img = (255*img).astype(np.uint8)
    viewer.add_image(img)
    layer = viewer.layers[-1]
    layer.metadata["arr"] = arr
    layer.metadata["ordertxt"] = ordertxt
    layer.name += ' - available arr'
    debug_reload()

# global parameters
@magicgui(
    thresh={'value':100, 'max':500},
    resolution={'value':256, 'max':8192},
    order={'value':11, 'max':50},
    )
def global_params(thresh=100, resolution=256, order=10, save_location=pathlib.Path('dump/browser')): 
    # default param values are necessary otherwise options don't display
    # but are insignificant as the default param values are overwritten
    # by the magicgui dict values (also necessary)
    global RESOLUTION, SAVE_PATH, ORDER
    frctl.set_thresh(thresh)
    RESOLUTION = resolution
    SAVE_PATH = save_location
    ORDER = order


viewer = napari.Viewer()

@magicgui(
    image1={'label':'Start Image'},
    image2={'label':'End Image'},
    breaks={'value':20},
    new_resolution={'value':1024, 'max':8192},
)
def lerp_images(image1:Image, image2:Image, breaks=20, new_resolution=1024, ordertxt='rgb'):
    try:
        arr1 = image1.metadata["arr"]
        arr2 = image2.metadata["arr"]
    except:
        print("No array availbale")
        return
    global RESOLUTION
    if len(ordertxt) > 3:
        ordertxt = list('rgb')
        random.shuffle(ordertxt)
        ordertxt = ''.join(ordertxt)
    arr_list = anim.lerp(arr1, arr2, breaks)
    frames = []
    for arr in progress(tqdm.tqdm(arr_list)):
        img = frctl.julia_from_2Darray(arr, (new_resolution,new_resolution), frctl.bernstein)
        img = anim.colorswap(img, ordertxt)
        img = (255*img).astype(np.uint8)
        frames.append(img)
    viewer.add_image(np.array(frames))
    layer = viewer.layers[-1]
    layer.metadata["arr"] = arr_list
    layer.metadata["ordertxt"] = ordertxt
    
    layer.name += ' - available arr'

@magicgui()
def load_image_from_array(path=pathlib.Path(r'dump\browser\functions')):
    arr = np.load(path)
    ordertxt = list('rgb')
    random.shuffle(ordertxt)
    ordertxt = ''.join(ordertxt)
    img = frctl.julia_from_2Darray(arr, (RESOLUTION,RESOLUTION), frctl.bernstein)
    img = anim.colorswap(img, ordertxt)
    img = (255*img).astype(np.uint8)
    viewer.add_image(img)
    layer = viewer.layers[-1]
    layer.metadata["arr"] = arr
    layer.metadata["ordertxt"] = ordertxt
    layer.name += ' - available arr'

@magicgui(
    image={'label':'Image'},
    new_resolution={'value':1024, 'max':8192}
    )
def enhance(image:Image, new_resolution=1024):
    arr = image.metadata["arr"]
    ordertxt = image.metadata["ordertxt"]
    img = frctl.julia_from_2Darray(arr, (new_resolution,new_resolution), frctl.bernstein)
    img = anim.colorswap(img, ordertxt)
    img = (255*img).astype(np.uint8)
    viewer.add_image(img)
    layer = viewer.layers[-1]
    layer.metadata["arr"] = arr
    layer.metadata["ordertxt"] = ordertxt
    layer.name += ' - enhanced'

@viewer.bind_key('0', overwrite=True)
def add_to_existing(v=viewer):
    if not v:
        v = viewer
    viewer_next()


@viewer.bind_key('1', overwrite=True)
def save_selected(v=viewer):
    if not v:
        v = viewer
    for layer in viewer.layers.selection:
        if type(layer) != Image:
            continue
        np.save(f'{SAVE_LOCATION}/functions/{layer.name}.npy', layer.metadata["arr"])
        io.imsave(f'{SAVE_LOCATION}/images/{layer.name}.png', layer.data)

@viewer.bind_key('2', overwrite=True)
def save_gif(v=viewer):
    if not v:
        v = viewer
    for layer in viewer.layers.selection:
        if layer.data.shape == 0:
            continue
        gif = [pilimage.fromarray(img) for img in list(layer.data)]
        gif[0].save(f'{SAVE_LOCATION}/gifs/{layer.name}.gif', save_all=True, optimize=False, append_images=gif[1:], loop=0)

        

@viewer.bind_key('3', overwrite=True)
def clear_all(v=viewer):
    if not v:
        v = viewer
    viewer.layers.clear()


add_button = QPushButton('Add new image (0)')
add_button.clicked.connect(add_to_existing)

save_button = QPushButton('Save seletected images and arrays (1)')
save_button.clicked.connect(save_selected)

save_gif_button = QPushButton('Save seletected stack (2)')
save_gif_button.clicked.connect(save_gif)

clear_button = QPushButton('Clear all images (3)')
clear_button.clicked.connect(clear_all)


list_buttons = [add_button, save_button, save_gif_button, clear_button]

viewer.window.add_dock_widget(global_params,area = 'right', name='Global Parameters')
viewer.window.add_dock_widget(load_image_from_array,area = 'right', name='Load Image From Array')
viewer.window.add_dock_widget(enhance,area = 'right', name='Enhance Image')
viewer.window.add_dock_widget(lerp_images,area = 'right', name='Lerp Images')
viewer.window.add_dock_widget(list_buttons,area = 'bottom')


napari.run()

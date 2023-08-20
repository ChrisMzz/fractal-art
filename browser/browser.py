import napari
from napari.layers import Image # for magicgui and selection error handling
from napari.utils import progress
import tqdm
from qtpy.QtWidgets import QPushButton, QMessageBox
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

param_R = lambda t : 9*(1-t)*t**3
param_G = lambda t : 15*((1-t)**2)*t**2
param_B = lambda t : 8.5*((1-t)**3)*t

# from https://theses.liacs.nl/pdf/2018-2019-JonckheereLSde.pdf


def func_gen():
    while True: # I'm so sorry
        yield anim.random_function_array(ORDER)

gene = func_gen()

def debug_reload():
    viewer.add_image(np.zeros((2,2)))
    del viewer.layers[-1]


def viewer_next():
    arr = next(gene)
    img = frctl.julia_from_2Darray(arr, (RESOLUTION,RESOLUTION), frctl.parametric_cmap)
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
    call_button='Set New Parameters',
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
        img = frctl.julia_from_2Darray(arr, (new_resolution,new_resolution), frctl.parametric_cmap)
        img = anim.colorswap(img, ordertxt)
        img = (255*img).astype(np.uint8)
        frames.append(img)
    viewer.add_image(np.array(frames))
    layer = viewer.layers[-1]
    layer.metadata["arr"] = arr_list
    layer.metadata["ordertxt"] = ordertxt
    
    layer.name += ' - available arr'

@magicgui(call_button='Load')
def load_image_from_array(path=pathlib.Path(r'dump\browser\functions')):
    arr = np.load(path)
    ordertxt = list('rgb')
    random.shuffle(ordertxt)
    ordertxt = ''.join(ordertxt)
    img = frctl.julia_from_2Darray(arr, (RESOLUTION,RESOLUTION), frctl.parametric_cmap)
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
    img = frctl.julia_from_2Darray(arr, (new_resolution,new_resolution), frctl.parametric_cmap)
    img = anim.colorswap(img, ordertxt)
    img = (255*img).astype(np.uint8)
    viewer.add_image(img)
    layer = viewer.layers[-1]
    layer.metadata["arr"] = arr
    layer.metadata["ordertxt"] = ordertxt
    layer.name += ' - enhanced'



@magicgui(call_button='Make New Parametric Functions Layer')
def make_param_functions_layer():
    viewer.add_image(np.zeros((2,2)))
    instructions = QMessageBox()
    instructions.setText('Make a New Parametric Functions layer.\n\nIn the napari console, set your `param_R`, `param_G`, and `param_B` functions into the `viewer.layers[-1].metadata` dictionary.\n\nExample : \n`viewer.layers[-1].metadata["param_R"] = lambda t : 9*(1-t)*t**3`\n\nMake sure this layer is at the top of the layers list before you push the new parametric functions.')
    instructions.setWindowTitle('Instructions')
    instructions.exec()


@magicgui(call_button='Push New Parametric Functions')
def push_param_functions():
    try:
        param_R = viewer.layers[-1].metadata["param_R"]
        param_G = viewer.layers[-1].metadata["param_G"]
        param_B = viewer.layers[-1].metadata["param_B"]
        frctl.set_param('R', param_R)
        frctl.set_param('G', param_G)
        frctl.set_param('B', param_B)
    except:
        return



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
viewer.window.add_dock_widget(make_param_functions_layer, area = 'bottom')
viewer.window.add_dock_widget(push_param_functions, area = 'bottom')



napari.run()
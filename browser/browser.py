import napari
from napari.layers import Image # for magicgui and selection error handling
from napari.utils import progress # still useful, not implemented in viewer window yet
import tqdm
from qtpy.QtWidgets import QPushButton, QMessageBox
from magicgui import magicgui
import pathlib # to include paths in magicgui widgets
from PIL import Image as pilimage
from zipfile import ZipFile
import sys, os, json

sys.path.insert(0, '../lib')
import animator as anim
import fractalize as frctl
import utility as util
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import random

param_layer_message_shown = False
THRESH = 50
frctl.set_thresh(THRESH)
RESOLUTION = 256
SAVE_LOCATION = 'dump'
ORDER = 11

param_R = lambda t : 9*(1-t)*t**3
param_G = lambda t : 15*((1-t)**2)*t**2
param_B = lambda t : 8.5*((1-t)**3)*t
cmap_dict = {
    "rc":9, "gc":15, "bc":8.5,
    "rlp":3, "glp":2, "blp":1,
    "rrp":1, "grp":2, "brp":3
}

# from https://theses.liacs.nl/pdf/2018-2019-JonckheereLSde.pdf


def func_gen():
    while True: # I'm so sorry
        yield anim.random_function_array(ORDER+1) # n-th order series expansion has n+1 terms

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
def global_params(thresh=100, resolution=256, order=10, save_location=pathlib.Path('dump')): 
    # default param values are necessary otherwise options don't display
    # but are insignificant as the default param values are overwritten
    # by the magicgui dict values (also necessary)
    global RESOLUTION, SAVE_LOCATION, ORDER, THRESH
    THRESH = thresh
    frctl.set_thresh(THRESH)
    RESOLUTION = resolution
    SAVE_LOCATION = save_location
    ORDER = order


viewer = napari.Viewer()

def load_frctl(path):
    global RESOLUTION, SAVE_LOCATION, ORDER
    with ZipFile(path) as zipfile:
        metadata_file = open(zipfile.extract('metadata.json'))
        metadata = json.load(metadata_file)
        metadata_file.close()
        rlp, rrp, glp, grp, blp, brp = [float(metadata["cmap_dict"][key]) for key in 
                                        ("rlp", "rrp", "glp", "grp", "blp", 'brp')]
        rc, gc, bc = [float(metadata["cmap_dict"][key]) for key in ("rc","gc","bc")]
        R, G, B = (rc, rlp, rrp), (gc, glp, grp), (bc, blp, brp)
        temp_param = []
        for canal in metadata["ordertxt"]:
            if canal == "r" or canal == "R": temp_param.append(R)
            if canal == "g" or canal == "G": temp_param.append(G)
            if canal == "b" or canal == "B": temp_param.append(B)
        (rc, rlp, rrp), (gc, glp, grp), (bc, blp, brp) = temp_param
        os.remove(zipfile.extract('metadata.json'))
        if metadata['format'] == 'tif':
            viewer.add_image(io.imread(zipfile.extract('image.tif')), name=metadata['name'])
            os.remove(zipfile.extract('image.tif'))
        else:
            viewer.add_image(io.imread(zipfile.extract('image.png')), name=metadata['name'])
            os.remove(zipfile.extract('image.png'))
        viewer.layers[-1].metadata["arr"] = np.load(zipfile.extract('function.npy'))
        os.remove(zipfile.extract('function.npy'))
        RESOLUTION, ORDER = metadata["resolution"], metadata["order"]
    

# to open files
if len(sys.argv) > 1:
    load_frctl(sys.argv[1])


@magicgui(
    image1={'label':'Image 1'},
    image2={'label':'Image 2'},
    breaks={'value':20},
    new_resolution={'value':256, 'max':8192},
)
def lerp_images(image1:Image, image2:Image, breaks=20, new_resolution=256, ordertxt='rgb'):
    try:
        img1 = image1.metadata["arr"]
        img2 = image2.metadata["arr"]
    except:
        print("No array availbale")
        return
    global RESOLUTION
    if len(ordertxt) > 3:
        ordertxt = list('rgb')
        random.shuffle(ordertxt)
        ordertxt = ''.join(ordertxt)
    arr_list = anim.lerp_projector(img1, img2, breaks) # make list of lerps to compute
    # thanks to https://stackoverflow.com/a/62109249/17091581
    bar = tqdm.tqdm(total=np.zeros(arr_list.shape[:-2]).size)
    p_bar = progress(bar)
    p_bar.display()
    space = anim.fill(arr_list, new_resolution, ordertxt, bar) # compute julia set images of lerps into a new array
    viewer.add_image(space)
    layer = viewer.layers[-1]
    layer.metadata["arr"] = arr_list
    layer.metadata["ordertxt"] = ordertxt
    layer.name += ' - available arr'

@magicgui(call_button='Load')
def load_image_from_array(path=pathlib.Path(r'dump')):
    #print(path.absolute().as_posix())
    # thanks guys
    # https://python-forum.io/thread-9077.html
    if path.absolute().as_posix()[-3:] == 'npy':
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
    elif path.absolute().as_posix()[-5:] == 'frctl':
        load_frctl(path)

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

# saving my life : https://stackoverflow.com/a/7821917/17091581
#@magicgui(call_button='Random Parametric Functions')
@viewer.bind_key('r', overwrite=True)
def random_param_functions(v=viewer):
    global param_layer_message_shown, cmap_dict
    if not v:
        v = viewer
    global param_R, param_G, param_B, THRESH
    rlp, rrp, glp, grp, blp, brp = np.random.rand(6)*4.9+0.1
    R = lambda t :  (1-t)**rrp*t**rlp
    G = lambda t :  (1-t)**grp*t**glp
    B = lambda t :  (1-t)**brp*t**blp
    x = np.linspace(0,1,50)
    rc, gc, bc = 1/max(R(x)), 1/max(G(x)), 1/max(B(x))
    param_R = lambda t : rc*(1-t)**rrp*t**rlp
    param_G = lambda t : gc*(1-t)**grp*t**glp
    param_B = lambda t : bc*(1-t)**brp*t**blp
    cmap_dict["rc"], cmap_dict["gc"], cmap_dict["bc"] = rc, gc, bc
    cmap_dict["rlp"], cmap_dict["glp"], cmap_dict["blp"] = rlp, glp, blp
    cmap_dict["rrp"], cmap_dict["grp"], cmap_dict["brp"] = rrp, grp, brp
    frctl.set_param('R', param_R)
    frctl.set_param('G', param_G)
    frctl.set_param('B', param_B)
    
    viewer.layers.clear()
    viewer_next()
    im = viewer.layers[-1].data
    im = im.transpose(2,0,1)[0]/255 # layer data is array where values are in [0,255]
    res = frctl.parametric_cmap(None, im)
    x = np.linspace(0,1,1000)
    fig, [[axTL, axTR], [axBL, axBR]] = plt.subplots(2,2)
    cmap = np.array([[[param_R(t), param_G(t), param_B(t)] for t in x] for _ in x])
    axTL.plot(x, param_R(x), color='r')
    axTL.plot(x, param_G(x), color='g')
    axTL.plot(x, param_B(x), color='b')
    axTL.plot(x, (param_R(x)+param_G(x)+param_B(x))/3, color=(0,0,0), linestyle=':')
    axTL.set_title('RGB Colour Distribution')
    axBL.plot(x, param_R(x)*param_G(x), color=(1,1,0))
    axBL.plot(x, param_G(x)*param_B(x), color=(0,1,1))
    axBL.plot(x, param_R(x)*param_B(x), color=(1,0,1))
    axBL.plot(x, (param_R(x)+param_G(x)+param_B(x))/3, color=(0,0,0), linestyle=':')
    axBL.set_title('CYM Colour Distribution')
    axTR.imshow(cmap, extent=[0,1,0,1])
    axTR.set_title('Colourmap Result')
    axTL.set_ylim([0,1]), axBL.set_ylim([0,1])
    axTR.set_yticklabels(''), axBR.set_xticklabels(''), axBR.set_yticklabels('')
    axBR.imshow(res)
    axBR.set_title('Result Image')
    fig.set_figwidth(10)
    fig.set_figheight(8)
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    viewer.layers.clear()
    viewer.add_image(data)
    if not param_layer_message_shown:
        instructions = QMessageBox()
        instructions.setText('Just made a New Parametric Functions layer.\n\nIn the napari console, set your `param_R`, `param_G`, and `param_B` functions into the `viewer.layers[-1].metadata` dictionary if you want to set those manually.\n\nExample : \n`viewer.layers[-1].metadata["param_R"] = lambda t : 9*(1-t)*t**3`\n\nMake sure this layer is at the top of the layers list before you push the new parametric functions.')
        instructions.setWindowTitle('Instructions')
        instructions.exec()
        param_layer_message_shown = True

@viewer.bind_key('0', overwrite=True)
def add_to_existing(v=viewer):
    if not v:
        v = viewer
    viewer_next()


@viewer.bind_key('1', overwrite=True)
def save_selected(v=viewer):
    global RESOLUTION, SAVE_LOCATION, ORDER, cmap_dict
    if not v:
        v = viewer
    for layer in viewer.layers.selection:
        if type(layer) != Image:
            continue
        np.save(f'function.npy', layer.metadata["arr"])
        try:
            file_format = 'png'
            io.imsave(f'image.png', layer.data)
        except: # image is not 2D
            file_format = 'tif'
            io.imsave(f'image.tif', layer.data)
        with open(f'metadata.json', 'w') as metadata:
            json.dump({
                "cmap_dict":cmap_dict,
                "ordertxt":layer.metadata["ordertxt"],
                "resolution":RESOLUTION, "order":ORDER, 
                "name":layer.name, "format":file_format}, metadata)
        with ZipFile(f'{SAVE_LOCATION}/{layer.name}.frctl', 'w') as file:
            file.write(f'function.npy')
            file.write(f'image.{file_format}')
            file.write(f'metadata.json')
    os.remove('function.npy'), os.remove('metadata.json')
    if os.path.exists('image.png'):os.remove('image.png')
    if os.path.exists('image.tif'):os.remove('image.tif')
    
    
    
        
        

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

save_gif_button = QPushButton('Save seletected as GIF (2)')
save_gif_button.clicked.connect(save_gif)

clear_button = QPushButton('Clear all images (3)')
clear_button.clicked.connect(clear_all)

random_param_button = QPushButton('Make random parametric functions layer (r)')
random_param_button.clicked.connect(random_param_functions)


list_buttons = [add_button, save_button, save_gif_button, clear_button]

viewer.window.add_dock_widget(global_params,area = 'right', name='Global Parameters')
viewer.window.add_dock_widget(load_image_from_array,area = 'right', name='Load Image From Array')
viewer.window.add_dock_widget(enhance,area = 'right', name='Enhance Image')
viewer.window.add_dock_widget(lerp_images,area = 'right', name='Lerp Images')
viewer.window.add_dock_widget(list_buttons,area = 'bottom')
viewer.window.add_dock_widget(random_param_button, area = 'bottom')
viewer.window.add_dock_widget(push_param_functions, area = 'bottom')



napari.run()

import sys
sys.path.insert(0, '../lib')
from skimage.io import imread
import fractalize as frctl
import matplotlib.pyplot as plt
import numpy as np


# default functions here
param_R = lambda t : 9*(1-t)*t**3
param_G = lambda t : 15*((1-t)**2)*t**2
param_B = lambda t : 8.5*((1-t)**3)*t


frctl.set_param('R', param_R)
frctl.set_param('G', param_G)
frctl.set_param('B', param_B)

im = imread(r'C:\Users\33783\OneDrive\Bureau\000Chris\Scolarité\Random Scripts\Python Scripts\fractal-art\browser\dump\browser\images\test11.png')
im = im.transpose(2,0,1)[0]

res = frctl.parametric_cmap(None, im)

fig, [[axTL, axTR], [axBL, axBR]] = plt.subplots(2,2)

x = np.linspace(0,1, 1000)


axTL.plot(x, param_R(x), color='r')
axTL.plot(x, param_G(x), color='g')
axTL.plot(x, param_B(x), color='b')
axTL.set_title('RGB Color Distribution')

axBL.plot(x, param_R(x)*param_G(x), color=(1,1,0))
axBL.plot(x, param_G(x)*param_B(x), color=(0,1,1))
axBL.plot(x, param_R(x)*param_B(x), color=(1,0,1))
axBL.set_title('CYM Color Distribution')

axTR.plot(x, (param_R(x)+param_G(x)+param_B(x))/3, color=(0,0,0))
axTR.set_title('Brightness Distribution')

axBR.imshow(res)
axBR.set_title('Result Image')

plt.show()



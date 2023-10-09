from skimage.io import imread
import sys
sys.path.insert(0, '../lib')
import fractalize as frctl
import matplotlib.pyplot as plt
import numpy as np


# default functions here
param_R = lambda t : 9*(1-t)*t**3
param_G = lambda t : 15*((1-t)**2)*t**2
param_B = lambda t : 8.5*((1-t)**3)*t

param_R = lambda t : 12.95*t**2.8*(1-t)**1.3
param_G = lambda t : 32.37*t**1.8*(1-t)**3.7
param_B = lambda t : 3.86*t**2.5*(1-t)**0.5

param_R = lambda t : 7.79*t**1.7*(1-t)**1.3
param_G = lambda t : 10.18*t**2.8*(1-t)**1.1
param_B = lambda t : 50.9*t**1.8*(1-t)**5





frctl.set_param('R', param_R)
frctl.set_param('G', param_G)
frctl.set_param('B', param_B)

im = imread(r'C:\Users\33783\OneDrive\Bureau\000Chris\Scolarité\Random Scripts\Python Scripts\fractal-art\browser\dump\browser\images\test11.png')
im = im.transpose(2,0,1)[0]

res = frctl.parametric_cmap(None, im)

fig, [[axTL, axTR], [axBL, axBR]] = plt.subplots(2,2)

x = np.linspace(0,1,1000)

cmap = np.array([[[param_R(t), param_G(t), param_B(t)] for t in x] for _ in x])
print(cmap.shape)
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


#fig.savefig('example_params.png', dpi=300, format='png')
plt.show()




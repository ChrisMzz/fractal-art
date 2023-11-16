#%%
import numpy as np
import matplotlib.pyplot as plt
from colorsys import hls_to_rgb

pi = np.pi
e = np.exp(1)
THRESH = 100

param_R = lambda t : 9*(1-t)*t**3
param_G = lambda t : 15*((1-t)**2)*t**2
param_B = lambda t : 8.5*((1-t)**3)*t


# from https://theses.liacs.nl/pdf/2018-2019-JonckheereLSde.pdf


def set_param(param, f):
    global param_R, param_G, param_B
    if param == 'r' or param == 'R':
        param_R = f
    if param == 'g' or param == 'G':
        param_G = f
    if param == 'b' or param == 'B':
        param_B = f
    return


def set_thresh(thresh):
    global THRESH
    THRESH = thresh

def mult(z, n):
    mult = 1
    for _ in range(n):
        mult *= z
    return mult

def polynomialize(arr):
    return lambda x : sum([arr[i]*mult(x,i) for i in range(len(arr))])

def reduce(n):
    try:
        result = n/3**int(np.log(n)/np.log(3))
    except:
        return np.NaN # was already NaN
    return result/3


def julia_on_point(z, f):
    z0 = z
    esc_array = np.zeros(shape=np.array(z).shape)+THRESH
    for esc in range(THRESH):
        z0 = f(z0)
        esc_array[np.transpose(np.abs(z0) < 1e200)] -= 1
    return z0, esc_array

def array_to_complex(arr):
    return [arr[0][i] + arr[1][i]*1j for i in range(len(arr[0]))]

def julia(f, shape=(512,512)):
    h, w = shape
    x,y = np.ogrid[-2:2:w*1j, -2:2:h*1j]
    z = x + 1j*y
    return julia_on_point(z, f)

# colorings

def hls_dc(z, esc):
    h = (np.angle(z) + pi)  / (2 * pi) + 0.5
    l = np.vectorize(reduce)(np.abs(z))**1.1
    s = 1
    c = np.vectorize(hls_to_rgb)(h,l,s)
    c = np.array(c)
    c = c.transpose(2,1,0)
    return c

def bw_coloring(z, esc): # only brightness of hls
    return (np.vectorize(reduce)(np.abs(z))**1.1).transpose()


def parametric_cmap(z, esc):
    global param_R, param_G, param_B
    t = esc/(THRESH-1)
    c = np.array([param_R(t), param_G(t), param_B(t)])
    c = np.transpose(c, (1,2,0))
    return c


# end of colorings


def julia_from_2Darray(arr, shape=(512,512), coloring=bw_coloring):
    z, esc = julia(polynomialize(array_to_complex(arr)), shape)
    return coloring(z, esc)

def julia_from_array(arr, shape=(512,512), coloring=bw_coloring):
    z, esc = julia(polynomialize(arr), shape)
    return coloring(z, esc)








# %%

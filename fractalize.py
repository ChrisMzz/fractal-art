#%%
import numpy as np
import matplotlib.pyplot as plt
from colorsys import hls_to_rgb
import pdb

pi = np.pi
e = np.exp(1)


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
    for _ in range(50):
        z0 = f(z0)
    return z0

def array_to_complex(arr):
    return [arr[0][i] + arr[1][i]*1j for i in range(len(arr[0]))]

def julia(f, shape=(512,512)):
    h, w = shape
    x,y = np.ogrid[-2:2:w*1j, -2:2:h*1j]
    z = x + 1j*y
    return julia_on_point(z, f)

# colorings

def hls_dc(z):
    h = (np.angle(z) + pi)  / (2 * pi) + 0.5
    l = np.vectorize(reduce)(np.abs(z))**1.1
    s = 1
    c = np.vectorize(hls_to_rgb)(h,l,s)
    c = np.array(c)
    c = c.transpose(2,1,0)
    return c

def bw_coloring(z): # only brightness of hls
    return (np.vectorize(reduce)(np.abs(z))**1.1).transpose()

def julia_from_2Darray(arr, shape=(512,512), coloring=bw_coloring):
    return coloring(julia(polynomialize(array_to_complex(arr)), shape))

def julia_from_array(arr, shape=(512,512), coloring=bw_coloring):
    return coloring(julia(polynomialize(arr), shape))


if __name__ == '__main__':
    image = julia_from_2Darray([[0.2,0,1],[0.1,0,0]])

    plt.imshow(image)
    plt.show()






# %%

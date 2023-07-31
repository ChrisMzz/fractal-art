#%%
import numpy as np
import matplotlib.pyplot as plt
from colorsys import hls_to_rgb
import pdb

pi = np.pi
e = np.exp(1)
THRESH = 100


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

def bernstein(z, esc):
    t = esc/(THRESH-1)
    # from https://theses.liacs.nl/pdf/2018-2019-JonckheereLSde.pdf
    r = lambda t : 9*(1-t)*t**3
    g = lambda t : 15*((1-t)**2)*t**2
    b = lambda t : 8.5*((1-t)**3)*t
    c = np.array([r(t),g(t),b(t)])
    c = np.transpose(c, (1,2,0))
    return c

def julia_from_2Darray(arr, shape=(512,512), coloring=bw_coloring):
    z, esc = julia(polynomialize(array_to_complex(arr)), shape)
    return coloring(z, esc)

def julia_from_array(arr, shape=(512,512), coloring=bw_coloring):
    z, esc = julia(polynomialize(arr), shape)
    return coloring(z, esc)


if __name__ == '__main__':
    import utility
    from skimage import io
    #func_arr = [[-0.8,0,1],[0.156,0,0]]
    #sinus = lambda x : [(0,1)[n%2==1]*(-1,1)[n%4==1]*x**n/utility.factorial(n) for n in range(11)]
    #print(sinus(1))
    #func_arr = [sinus(1),[0 for _ in range(11)]]
    #plt.plot(np.linspace(0,8,1000),polynomialize(array_to_complex(func_arr))(np.linspace(0,8,1000)))
    #plt.show()
    
    func_arr = [1-2*np.random.rand(11), 1-2*np.random.rand(11)]
    
    image = julia_from_2Darray(func_arr, (1024,1024), coloring=bernstein)
    #image = utility.set_nan_to_zero(image)
    plt.imshow(image)
    plt.show()
    io.imsave("itsabwok.png", image)
    






# %%

from ...lib import utility as util
from ...lib import fractalize as frctl
import matplotlib.pyplot as plt
import numpy as np


def real_project(arr):
    return frctl.polynomialize(arr[0])

def im_project(arr):
    return frctl.polynomialize(arr[1])


def plot_on_interval(f, interval, ax=plt, **kwargs):
    x = np.linspace(interval[0], interval[1], 1000)
    ax.plot(x, f(x), **kwargs)


def plot_all_on_interval(arr, interval):
    real = real_project(arr)
    im = im_project(arr)
    fig, (axreal, axim) = plt.subplots(1,2)
    plot_on_interval(real, interval, axreal, color='b', label='real part')
    plot_on_interval(im, interval, axim, color='r', label='imaginary part')
    fig.legend()
    plt.show()
    
    


if __name__ == "__main__":

    arr = np.load(r'C:\Users\33783\OneDrive\Bureau\000Chris\Scolarité\Random Scripts\Python Scripts\fractal-art\browser\dump\browser\functions\spiral1.npy')

    f = im_project(arr)

    plot_on_interval(f, [-1,1], color='r')
    plot_all_on_interval(arr, [-1,1])


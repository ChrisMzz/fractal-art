
# `fractal-art`, a passion project about the artistic value of function spaces

The project is split in many parts but the main takeaway so far is the napari browser I coded to view julia sets of some polynomial functions.

Most of the functions you use on a daily basis can be approximated by polynomials. This holds true for the complex plane, but the differences between the real thing and the approximate generally appear more clearly.

However, that doesn't stop us from appreciating how weird-looking some sets are, and if you look far and wide enough you'll probably see remnants of other big mathematical objects such as the Fibonacci sequence / golden ratio.

I also wanted to see if we could train a neural network to find functions that look like certain shapes ? But that didn't pan out too well, probably because I'm new to neural networks overall (help will be appreciated greatly!).

## Browser

Here, I'll explain everything you need to know about the browser.

I coded the browser so I'd be able to cycle through random Julia sets quicker, but as it could serve others for the same purpose, I thought I'd make it as user-friendly as possible.

However, I couldn't code a napari browser without all the dependencies listed below, as I need most of these for the built-in functionalities.

### Dependencies (for development)

- `napari`, install with :
```bat
python -m pip install "napari[all]"
```
- `magicgui` which depends on `qtpy`, install with :
```bat
pip install magicgui[pyqt5]
pip install QtPy
```
- `PIL`, the Python Image Library. I know `PIL` is discontinued, but `Pillow` doesn't support `import Image` anymore, and the [official documentation recommends using `from PIL import Image`](https://pillow.readthedocs.io/en/stable/installation.html#warnings). Install with :
```bat
pip install Pillow
```
- `scikit-image`, install with :
```bat
pip install scikit-image
```
- `numpy`, install with : 
```bat
pip install numpy
```
I also use `pathlib`, but that comes built into Python versions >= 3.4, so make sure your Python version includes `pathlib`.

#### For the fractal viewer 

To run the fractal viewer with Python, you'll need : 

`pygame` (versions 2.0.1 and up), and `PyOpenGL`, both installable with pip.


### How to use

So far I've only released a Windows executable file, I'm not sure I'll cover MacOS and Linux support as I'm fairly new to releases overall.

When opened, the browser should look something like this :

![](https://github.com/ChrisMzz/fractal-art/blob/main/readme_dump/test_viewer.PNG)
*obsolete image, change soon*

If you don't have a NumPad, you can use the buttons, but just in case you do have one, here are some shortcuts : 
 - 0 creates a random image using current settings (those can be changed in the topright widget)
 - 1 saves current image in a frctl file (that depends on the array shape) to be opened in other instances
 - 2 saves a gif of the 1D lerp selected (only for 1D lerps!)
 - 3 clears viewer

I also implemented a "R key" shortcut to clear the viewer and randomize colourmaps.
*Note : custom colourmaps can be assigned manually. A "tutorial" for this is displayed the first time you randomize the cmaps.*

You can lerp two images of same shape together using the lerp widget, which yields a higher-dimensional image. Be wary, this can take a lot of time. To accomodate this, I implemented a progress bar that displays in the window that doesn't have any GUI (this displays how many images it has to compute, so you can always shut down the application if you think it will ruin your computer's CPU).

You can save images as `.frctl` files ( a "fractal file" containing metadata, array data and the actual image).
You can then load `.npy` or `.frctl` files (`npy` files need to be arrays of shape `(2,n)` representing a Taylor expansion of the function of order $n$, separating real and imaginary parts).
`frctl` files can also be opened outside of the browser, you can open them using the explorer executable or the browser executable. I recommend setting the explorer executable as the default application.
*If you want to set the explorer executable as the default application for these in the **Windows** registry, I included a regkey file in this repository where you only have to change `%directory%` to the directory in which the executable is.*

Of course, if you like a function but don't want to save it, just view it in higher resolution (or lower resolution), you can "enhance" a selected image.

The parametric functions representing the colourmaps are also shuffled for more colour variety, so if you want to fix a certain `rgb` function order, set the order in a lerp (you can even do this for singular images if you choose a lerp size of 1, of an image with itself).


### Pretty gifs

![](https://github.com/ChrisMzz/fractal-art/blob/main/browser/dump/gifs/giftesting.gif)


### Parametric Function Editor for Colours (Visualiser)

![](https://github.com/ChrisMzz/fractal-art/blob/main/readme_dump/default_params.png)

![](https://github.com/ChrisMzz/fractal-art/blob/main/readme_dump/example_params.png)

### Napari 3D Projection Viewer

![](https://github.com/ChrisMzz/fractal-art/blob/main/readme_dump/3D_view_1.PNG)

![](https://github.com/ChrisMzz/fractal-art/blob/main/readme_dump/galaxystack.gif)

### Napari N-dimensional Projection Viewer





# `fractal-art`, a passion project about the artistic value of function spaces

The project is split in many parts but the main takeaway so far is the napari browser I coded to view julia sets of some polynomial functions.

Most of the functions you use on a daily basis can be approximated by polynomials. This holds true for the complex plane, but the differences between the real thing and the approximate generally appear more clearly.

However, that doesn't stop us from appreciating how weird-looking some sets are, and if you look far and wide enough you'll probably see remnants of other big mathematical objects such as the Fibonacci sequence / golden ratio.

I also wanted to see if we could train a neural network to find functions that look like certain shapes ? But that didn't pan out too well, probably because I'm new to neural networks overall (help will be appreciated greatly!).

## Browser

Here, I'll explain everything you need to know about the browser.

I coded the browser so I'd be able to cycle through random Julia sets quicker, but as it could serve others for the same purpose, I thought I'd make it as user-friendly as possible.

However, I couldn't code a napari browser without all the dependencies listed below, as I need most of these for the built-in functionalities.

### Dependencies

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


### How to use

*work in progress*



### Pretty gifs

![](https://github.com/ChrisMzz/fractal-art/blob/main/browser/dump/browser/gifs/giftesting.gif)





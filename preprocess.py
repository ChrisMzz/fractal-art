import skimage


PATH_TO_IMAGE = fr'DATA/euler.jpg'

SAVE_PATH = fr'DATA/test2.jpg'


image = skimage.io.imread(PATH_TO_IMAGE)


def webify(image, low_sigma, high_sigma):
    image = skimage.filters.difference_of_gaussians(image, low_sigma, high_sigma)
    image = skimage.morphology.skeletonize(image)
    image = image > 0
    return image

def process(image):
    layer1 = webify(image, 2, 4)
    layer2 = webify(image, 9, 10)
    mask = skimage.filters.gaussian(layer2, 2)
    processed = ((mask > 0) * layer1 + layer2) > 0
    return processed


skimage.io.imsave(SAVE_PATH, process(image))


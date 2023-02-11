import numpy as np
import cv2 as cv
import warnings

try:
    import napari
except ImportError:
    warnings.warn("The package napari is not installed. Install napari to enable visualization features. Attention: installation of napari differs from machine to machine. Make sure to choose the right installation command for your machine.")
    _has_napari = False
else:
    _has_napari = True

def visualize_all_list_napari(numpy_img_list: np.ndarray,names):
    """
    :param numpy_img_list: list containing different images to be visualized
    """
    with napari.gui_qt():
        viewer = napari.Viewer()
        for i, img in enumerate(numpy_img_list):
            viewer.add_image(img, name=names[i])

def add_bounding_boxes(original_img, stats):
    """
    Add white rectangles around bacilli, based on conected components

    :param image: image with bacilli to be boxed
    :param coordinates:  coordinates of the center of the bacillus
    """
    img_copy = original_img.copy()
    for i in range(1, len(stats)):
        x = stats[i][0] - 5
        # x_max = coordinates[i][0]
        y = stats[i][1] - 5
        # y_max = coordinates[i][1]
        h = stats[i][3]
        w = stats[i][2]
        cv.rectangle(img_copy, (x, y), (x + w + 10, y + h + 10), (5000, 255, 255), 1)
    return img_copy

def is_blurry_laplacian(image):
    #compute laplacian of image
    laplacian = cv.Laplacian(image, cv.CV_64F)
    #compute variance of laplacian
    measure=laplacian.var()/np.mean(image)
    #print(measure)
    #if meausure is less than 109, image is blurry
    if measure < 109.8:
        return True
    else:
        return False


def is_blurry(image):
    #maybe find better method but we need something like this
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    #find mean of magnitude spectrum
    mean = np.mean(magnitude_spectrum)
    #print(mean)

    if mean < 220:
        return True
    else:
        return False
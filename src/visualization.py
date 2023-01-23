import napari
import cv2 as cv


def visualize_all_list_napari(numpy_img_list, names):
    """
    :param numpy_img_list: list containing different images to be visualized
    :param names: list containing names of the images
    """
    with napari.gui_qt():
        viewer = napari.Viewer()
        for i, img in enumerate(numpy_img_list):
            viewer.add_image(img, name=names[i])


def add_bounding_boxes(original_img, stats):
    """
    Add white rectangles around bacilli, based on conected components

    :param original_img: original image
    :param stats: stats from connected components
    """
    img_copy = original_img.copy()
    for i in range(1, len(stats)):
        x = stats[i][0] - 5
        y = stats[i][1] - 5
        h = stats[i][3]
        w = stats[i][2]
        cv.rectangle(img_copy, (x, y), (x + w + 10, y + h + 10), (5000, 255, 255), 1)
    return img_copy



import numpy as np
import cv2 as cv


def clean_connected_components(whole_tile):
    """ Clean image with 2 approaches:
    -delete connected components that have up to 2 pixels
    -connect bacilli that are separated by just one black pixel

    parameters
    ----------
    whole_tile:
        image to be cleaned

    returns
    -------
    whole_tile:
        cleaned image
    num_labels:
        number of connected components
    stats:
        stats of the connected components
    """
    # find connected components
    num_labels, labels_im, stats, centroids = cv.connectedComponentsWithStats(np.uint8(whole_tile), connectivity=8)
    # stats = x,y,w,h,area
    print("Number of connected components before cleaning: ", num_labels)
    # put to black connected components which area is equal to 1 or 2
    for i in range(1, num_labels):
        if stats[i][4] < 3:
            whole_tile[labels_im == i] = 0

    # connect the bacilli, by putting a white tile
    for i in range(1, whole_tile.shape[0] - 1):
        for j in range(1, whole_tile.shape[1] - 1):
            if whole_tile[i, j] == 0:
                if (whole_tile[i - 1, j] == 255 and whole_tile[i + 1, j] == 255) or \
                        (whole_tile[i, j - 1] == 255 and whole_tile[i, j + 1] == 255) \
                        or (whole_tile[i - 1, j - 1] == 255 and whole_tile[i + 1, j + 1]) \
                        or (whole_tile[i - 1, j + 1] == 255 and whole_tile[i + 1, j - 1] == 255) \
                        or (whole_tile[i - 1, j] == 255 and whole_tile[i + 1, j + 1] == 255) \
                        or (whole_tile[i - 1, j + 1] == 255 and whole_tile[i + 1, j] == 255) \
                        or (whole_tile[i - 1, j] == 255 and whole_tile[i + 1, j - 1] == 255) \
                        or (whole_tile[i - 1, j - 1] == 255 and whole_tile[i + 1, j] == 255) \
                        or (whole_tile[i, j - 1] == 255 and whole_tile[i + 1, j + 1] == 255) \
                        or (whole_tile[i, j - 1] == 255 and whole_tile[i - 1, j + 1] == 255) \
                        or (whole_tile[i, j + 1] == 255 and whole_tile[i + 1, j - 1] == 255) \
                        or (whole_tile[i, j + 1] == 255 and whole_tile[i - 1, j - 1] == 255):
                    whole_tile[i, j] = 255
    num_labels, labels_im, stats, centroids = cv.connectedComponentsWithStats(np.uint8(whole_tile), connectivity=8)

    print("Number of connected components after cleaning: ", num_labels)
    return whole_tile, num_labels, stats


class Postprocessing:
    """Class that cleans imprecisions after thresholding.
    Different thresholding algorithms have different cleaning methods.
    Split otsu thresholding is the only one that needs to split the image into tiles.
    The adaptive methods only need morphological operations.

     attributes
     ----------
    img:
        image to be cleaned
    config:
        dictionary with the parameters
    tiles:
        list with the different small tiles

    methods
    -------
    split_into_tiles(tile_size=16):
        split image into tiles of shape tile_size * tile_size
    cleaning_tiles():
        Clean the small tiles of the image
    check_image(img: np.ndarray):
        For every sub-image we check if there is a bacilli or not
    reconstruct_image():
        Reconstruct the image from the clean sub-tiles
    remove_noise():
        Remove noise from the image
    apply():
        Apply the postprocessing to the image
    """

    def __init__(self, img, config):
        """
        parameters
        ----------
        img:
            image to be cleaned
        config:
            dictionary with the parameters
        """
        self.img = img
        self.config = config
        # split image into tiles if we have otsu split algorithm
        if config['algorithm'] == 'otsu':
            self.tiles = self.split_into_tiles(tile_size=self.config['tile_size'])

    # -----------------------------------CLEANING FOR OTSU THRESHOLDING-----------------------------------

    def split_into_tiles(self, tile_size=16):
        """ split image into tiles of shape tile_size * tile_size

        parameters
        ----------
        tile_size:
            dimensions of single tiles

        returns
        -------
        tiles:
            list with all the tiles
        """
        print("Splitting image into tiles...")
        tiles = []
        for i in range(0, self.img.shape[0], tile_size):
            for j in range(0, self.img.shape[1], tile_size):
                tile = self.img[i:i + tile_size, j:j + tile_size]
                tiles.append(tile)
        return tiles

    def cleaning_tiles(self):
        """ Clean the tiles of the image, based on the number of black pixels in the tile

        returns
        -------
        cleaned_tiles:
            list with the cleaned tiles
        """
        print("Cleaning tiles...")
        cleaned_tiles = []
        for t in self.tiles:
            # check if image is not a bacilli
            # the tile doesn't contain a bacilli
            if self.check_image(t):
                t[t > 0] = 0
                cleaned_tiles.append(t)
            # the tile contains a bacilli
            else:
                cleaned_tiles.append(t)
        return cleaned_tiles

    def check_image(self, img: np.ndarray):
        """ For every sub-image we check if its worth keeping or not
        based on the number_of_black_pixels

        parameters
        ----------
        img:
            image to be checked

        returns
        -------
        True:
            if the image is background
        False:
            if the image is a bacilli
        """
        number_of_black_pixels = self.config['number_of_black_pixels']
        # we have a bacilli
        if np.sum(img == 0) > number_of_black_pixels:
            return False
        # we have background
        else:
            return True

    def reconstruct_image(self, tiles: list):
        """ Reconstruct the image from the clean sub-tiles

        parameters
        ----------
        tiles:
            list with the cleaned tiles

        returns
        -------
        whole_image:
            reconstructed image
        """
        x_tiles = self.config['x_tiles']
        y_tiles = self.config['y_tiles']
        whole_img = np.zeros((x_tiles * tiles[0].shape[0], y_tiles * tiles[0].shape[1]))
        for i in range(x_tiles):
            for j in range(y_tiles):
                whole_img[i * tiles[0].shape[0]:(i + 1) * tiles[0].shape[0],
                    j * tiles[0].shape[1]:(j + 1) * tiles[0].shape[1]] = tiles[i * y_tiles + j]
        return whole_img

    # -----------------------------------CLEANING FOR ADAPTIVE THRESHOLDING-----------------------------------

    # remove noise
    def remove_noise(self):
        """ Perform morphological opening and closing to remove noise

        returns
        -------
        closing:
            cleaned imag
        """

        # define kernel for opening
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))

        # perform morphological opening to remove background noise
        opening = cv.morphologyEx(self.img, cv.MORPH_OPEN, kernel)

        # perform morphological closing to close small holes inside foreground objects
        closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

        return closing

    def apply(self):
        """ Apply the postprocessing to the image

        returns
        -------
        whole_img_not_cleaned:
            image before cleaning
        whole_img_cleaned:
            image after cleaning
        num_bacilli:
            number of bacilli in the image
        """
        print("Applying postprocessing...")

        if self.config['algorithm'] == 'otsu':
            cleaned_tiles = self.cleaning_tiles()
            whole_img_not_cleaned = self.reconstruct_image(cleaned_tiles)
            whole_img_not_cleaned_copy = whole_img_not_cleaned.copy()
            whole_img_cleaned, num_bacilli, stats = clean_connected_components(whole_img_not_cleaned_copy)
            return whole_img_not_cleaned, whole_img_cleaned, num_bacilli - 1, stats

        elif self.config['algorithm'] == 'adaptive_gaussian':
            whole_img_cleaned = self.remove_noise()
            num_labels, labels_im, stats, centroids = cv.connectedComponentsWithStats(whole_img_cleaned, connectivity=8)
            return self.img, whole_img_cleaned, num_labels - 1, stats

        elif self.config['algorithm'] == 'hard':
            num_labels, labels_im, stats, centroids = cv.connectedComponentsWithStats(np.uint8(self.img),
                                                                                      connectivity=8)
            return self.img, self.img, num_labels - 1, stats

        elif self.config['algorithm'] == 'adaptive_mean':
            whole_img_cleaned = self.remove_noise()
            num_labels, labels_im, stats, centroids = cv.connectedComponentsWithStats(whole_img_cleaned, connectivity=8)
            return self.img, whole_img_cleaned, num_labels - 1, stats

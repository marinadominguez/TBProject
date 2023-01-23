import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from n_networks.neural_net import ChatGPT
import pandas as pd
import joblib
from utils import clean_stats


class Inference:
    """
    Predict the class of the images, bacilli or not, can use either:
    - network_prediction
    - stats_prediction
    - svm_prediction
    """
    def __init__(self, cropped_images, stats, final_image):
        """
        :param: cropped_images: images to be classified
        :param stats: stats of the images
        :param final_image: masked image
        """
        self.final_image = final_image
        self.cropped_images = cropped_images
        self.stats = stats
        # clean stats
        self.stats = clean_stats(self.stats)
        # load the model
        self.PATH = 'n_networks/model.pth'
        # initialize the model
        self.model = ChatGPT()
        # set parameters
        self.model.load_state_dict(torch.load(self.PATH))
        # get the dataset, with dataset loader
        dataset = self.get_dataset()
        inference_dataset = MyDataset(dataset)
        self.inference_dataset_loader = DataLoader(inference_dataset, batch_size=1, shuffle=False)

    def network_prediction(self):
        """
        Predict the class of the images, using the neural network,
        return arrays needed to draw the boxes in napari

        :return: red_boxes, green_boxes
        """
        # initialize prediction array
        predictions = np.array([])
        # iterate over the dataset and predict the class
        self.model.eval()
        with torch.no_grad():
            for i, data in enumerate(self.inference_dataset_loader):
                image = data
                image = image.to(torch.float32)
                image = image.view(1, 1, 50, 50)
                output = self.model(image)
                output = output.squeeze(1)
                if output > 0.5:
                    predictions = np.append(predictions, 1)
                else:
                    predictions = np.append(predictions, 0)
        # use get_boxes to get the boxes
        return self.get_boxes(predictions)

    def get_hu_moments(self):
        """
        Get elongation Hu-moment for every object in the image.

        :return: List of all elongation Hu-moments
        """
        hu_moments = np.array([])
        for i in range(1, self.stats.shape[0]):
            hu_moments = np.append(hu_moments, cv2.HuMoments(
                cv2.moments(self.final_image[self.stats[i][1]:self.stats[i][1]+self.stats[i][3],
                            self.stats[i][0]:self.stats[i][0]+self.stats[i][2]]))[2])
        return hu_moments

    def stats_prediction(self):
        """
        Predict the class of the images, using the stats,
        using the elongation Hu moment and the area of the object.

        :return: red_boxes, green_boxes
        """
        predictions = np.array([])
        # get elongation Hu-moments
        list_hu = self.get_hu_moments()
        # predict the class
        for i in range(0, list_hu.shape[0]):
            if list_hu[i] >= 5e-12:
                predictions = np.append(predictions, 1)
            else:
                predictions = np.append(predictions, 0)
            if self.stats[i][4] > 200:
                predictions[i] = 0
        return self.get_boxes(predictions)

    def svm_prediction(self):
        """
        Predict the class of the images, using a svm that was trained on the stats.

        :return: red_boxes, green_boxes
        """
        # drop coordinates from stats
        self.stats = self.stats[:, 2:]
        # create a stats dataframe
        df = pd.DataFrame(self.stats)
        # load the svm model
        loaded_model = joblib.load('svm_results/svm.pkl')
        # predict the class
        predictions = loaded_model.predict(df)
        return self.get_boxes(predictions)

    def get_boxes(self, predictions):
        """
        Get the boxes to draw in napari, based on the predictions.

        :param: predictions: array of predictions
        :return: red_boxes, green_boxes
        """

        red_boxes = np.array([[0, 0], [0, 0]])
        red_boxes = np.stack((red_boxes, red_boxes), axis=0)
        green_boxes = np.array([[0, 0], [0, 0]])
        green_boxes = np.stack((green_boxes, green_boxes), axis=0)
        # create a rectangle array
        for i in range(0, predictions.shape[0]):
            y = self.stats[i+1][0] - 5
            x = self.stats[i+1][1] - 5
            w = self.stats[i+1][3]
            h = self.stats[i+1][2]
            if predictions[i] == 0:
                red_boxes = np.concatenate((red_boxes, [np.array([[x, y], [x + w + 10, y + h + 10]])]), axis=0)

            else:
                green_boxes = np.concatenate((green_boxes, [np.array([[x, y], [x + w + 10, y + h + 10]])]), axis=0)
        # remove first two by two matrix that where added to initialize the array
        red_boxes = np.delete(red_boxes, 0, axis=0)
        red_boxes = np.delete(red_boxes, 0, axis=0)
        green_boxes = np.delete(green_boxes, 0, axis=0)
        green_boxes = np.delete(green_boxes, 0, axis=0)
        return red_boxes, green_boxes

    def get_dataset(self):
        """
        Create a dataset from the cropped images, to be used in the neural network.
        """
        dataframe = pd.DataFrame()
        for i in range(0, self.cropped_images.shape[0]):
            d = {'image': [self.cropped_images[i]]}
            df2 = pd.DataFrame(d)
            dataframe = pd.concat([dataframe, df2], ignore_index=True)
        return dataframe


class MyDataset(Dataset):
    """
    Dataset class for the neural network.
    """
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        img = self.data.iloc[index]['image']
        # change image values to be in 0,1 range instead of 0, 16000
        img = img / 16000

        return torch.tensor(img, dtype=torch.float32)
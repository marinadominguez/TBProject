import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import numpy as np


class BacilliNet(nn.Module):
    def __init__(self):
        super(BacilliNet, self).__init__()

        # 1st convolutional layer
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2)

        # 2nd convolutional layer
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2)

        # Fully connected layers
        self.fc1 = nn.Linear(in_features=64 * 12 * 12, out_features=1028)
        self.relu3 = nn.ReLU()
        self.dropout = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(in_features=1028, out_features=256)
        self.fc3 = nn.Linear(in_features=256, out_features=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 1st convolutional layer
        out = self.conv1(x)
        out = self.relu1(out)
        out = self.maxpool1(out)

        # 2nd convolutional layer
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.maxpool2(out)

        # Fully connected layers
        out = out.view(-1, 64 * 12 * 12)

        out = self.fc1(out)
        out = self.relu3(out)
        # out = self.dropout(out)
        out = self.fc2(out)
        out = self.relu3(out)

        out = self.fc3(out)
        out = self.sigmoid(out)

        return out


class ChatGPT(nn.Module):
    def __init__(self):
        super(ChatGPT, self).__init__()

        # 1st convolutional layer
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2)

        # 2nd convolutional layer
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2)

        # Fully connected layers
        self.fc1 = nn.Linear(in_features=64 * 12 * 12, out_features=512)
        self.relu3 = nn.ReLU()
        self.dropout = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(in_features=512, out_features=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 1st convolutional layer
        out = self.conv1(x)
        out = self.relu1(out)
        out = self.maxpool1(out)

        # 2nd convolutional layer
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.maxpool2(out)

        # Fully connected layers
        out = out.view(-1, 64 * 12 * 12)

        out = self.fc1(out)
        out = self.relu3(out)
        # out = self.dropout(out)
        out = self.fc2(out)
        out = self.sigmoid(out)

        return out


class ChatGPT(nn.Module):
    def __init__(self):
        super(ChatGPT, self).__init__()

        # 1st convolutional layer
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2)

        # 2nd convolutional layer
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2)

        # Fully connected layers
        self.fc1 = nn.Linear(in_features=64 * 12 * 12, out_features=512)
        self.relu3 = nn.ReLU()
        self.dropout = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(in_features=512, out_features=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 1st convolutional layer
        out = self.conv1(x)
        out = self.relu1(out)
        out = self.maxpool1(out)

        # 2nd convolutional layer
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.maxpool2(out)

        # Fully connected layers
        out = out.view(-1, 64 * 12 * 12)

        out = self.fc1(out)
        out = self.relu3(out)
        # out = self.dropout(out)
        out = self.fc2(out)
        out = self.sigmoid(out)

        return out


class MyDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        img = self.data.iloc[index]['image']
        img = np.array(img)
        # change image values to be in 0,1 range instead of 0, 16000
        # if img.max() > 0:
        #     img = img / img.max()
        # convert to uint4
        if np.max(img) - np.min(img) != 0:
            img = (img - np.min(img)) / (np.max(img) - np.min(img)) - 0.5

        return torch.tensor(img, dtype=torch.float32)
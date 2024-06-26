#based on: https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
from __future__ import print_function, division
import os
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
import pandas as pd

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        embedding, target = sample['embedding'], sample['target_class']
#         embedding, target = sample['embedding'], sample['target_class']
        return {'embedding': torch.from_numpy(embedding),
                'target_class': torch.from_numpy(target)}


class Emb_Workhours_Dataset(Dataset):
    """Dataset containing the embedding and the class 'hot' or 'cold' based on the temperature at that time."""

    def __init__(self, csv_file, train=True, transform=None, train_test_split=0.8, emb_header='emb', target_class='workhours'):
        csv_file = pd.read_csv(csv_file, sep=",")
        if train:
            
            self.emb_classes = csv_file[:int(len(csv_file)*train_test_split)].reset_index()
        else:
            self.emb_classes = csv_file[int(len(csv_file)*train_test_split):].reset_index()

        self.transform = transform
        self.emb_header = emb_header
        self.target_class = target_class

        if target_class == "https://interconnectproject.eu/example/Konstanz_HotCold":
            self.opsd = True
            self.classes = ['hot', 'cold']

        else:
            self.opsd = False

    def __len__(self):
        return len(self.emb_classes)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        # print("idx:", idx)
        target = self.emb_classes[self.target_class][idx]
        if self.opsd:
            for i in range(0, len(self.classes)):
                if target == self.classes[i]:
                    target = i
        target = np.array(target)
        
        sample = {'embedding': np.array([float(x.strip(' []')) for x in self.emb_classes[self.emb_header][idx].split(',')]), 
                  'target_class': target 
                 }
        if self.transform:
            sample = self.transform(sample)

        return sample
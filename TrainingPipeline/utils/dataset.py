import cv2
import torch
from PIL import Image
from torch.utils.data import Dataset


class FoodDataset(Dataset):
    def __init__(self, metadata, transforms, cat_names, data_path, augmentations=None):
        self.metadata = metadata
        self.transforms = transforms
        self.data_path = data_path
        self.augmentations = augmentations
        
    def __len__(self):
        return self.metadata.shape[0]
    
    def __getitem__(self, index):
        target = torch.as_tensor(int(self.metadata.loc[index, 'class']))
        image = cv2.imread(self.data_path + '/' + self.metadata.loc[index, 'image_path'])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        if self.augmentations is not None:
            image = self.augmentations(image=image)['image']
        
        return self.transforms(Image.fromarray(image)), target, image

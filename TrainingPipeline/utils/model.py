import torch.nn as nn
import torch.nn.functional as F

class FoodRecognitionModel(nn.Module):
    def __init__(self, backbone, out_features):
        super(FoodRecognitionModel, self).__init__()
        self.backbone = backbone
        self.batch_norm = nn.BatchNorm1d(num_features=backbone.fc.out_features)
        self.drop = nn.Dropout()
        self.fc = nn.Linear(backbone.fc.out_features, out_features)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        x = self.backbone(x)
        x = self.batch_norm(x)
        x = F.relu(x)
        x = self.drop(x)
        x = self.fc(x)
        x = self.softmax(x)

        return x

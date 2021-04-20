import torch
import numpy
import random

# use seed to ensure reproducibility
SEED = 1234
random.seed(SEED)
torch.random.manual_seed(SEED)
numpy.random.seed(SEED)

ROOT = 'C:/Users/bubur/Documents/FoodRecognition'

data_config = {
    'metadata_path' : ROOT + '/Food-101/meta/metadata.csv',
    'data_path' : ROOT + '/Food-101/data',

    'image_size' : (256, 256)
}

train_config = {
    'round_name' : 'resnet50_augmentations_Food101_multiclass_2',
    'debug' : False,
    'lr_finder' : False,

    'batch_size' : 32,
    'num_workers' : 4,
    'num_epochs' : 6,
    'lr' : 1e-4,
    'valid_step' : 400
}

results_path = ROOT + '/results/' + train_config['round_name']

results_config = {
    'results_path' : results_path,
    'checkpoints_path' : results_path + '/checkpoints', 
    'logs_path' : results_path + '/logs',
    'tensorboard_path' : results_path + '/tensorboard'
}

config = {**train_config, **data_config}
config = {**config, **results_config}
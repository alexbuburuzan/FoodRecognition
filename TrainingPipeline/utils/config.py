import torch
import numpy
import random

# use seed to ensure reproducibility
SEED = 1234
random.seed(SEED)
torch.random.manual_seed(SEED)
numpy.random.seed(SEED)

ROOT = 'FoodRecognition'

data_config = {
    'metadata_path' : ROOT + '/data/metadata.csv',
    'data_path' : ROOT + '/data',

    'image_size' : (256, 256)
}

train_config = {
    'round_name' : 'round_description',
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
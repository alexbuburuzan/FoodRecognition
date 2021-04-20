import os
import numpy as np
import yaml
import torch
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm

def create_files(path_list):
    """Creates non-existing files"""

    for path in path_list:
        if os.path.exists(path) is False:
            os.mkdir(path)


def save_logs(logs, path):
    """Saves the config dict in yaml format"""

    with open(path + '/{}.yaml'.format('config_logs'), 'w') as output_file:
        yaml.dump(logs, output_file)


def get_lr(optimizer):
    """Returns current learning rate of optimizer"""

    for param_group in optimizer.param_groups:
        return param_group['lr']


def save_model(epoch, model, optimizer, path):
    """Saves the state dict of the current model"""

    state_dict = model.state_dict()
    
    for key in state_dict.keys():
        state_dict[key] = state_dict[key].cpu()
        
    torch.save({
        'epoch': epoch,
        'state_dict': state_dict,
        'optimizer' : optimizer.state_dict()},
        path + '/{}.pth'.format(epoch))


def validate(model, valid_loader, valid_epoch, criterion, writer, device):
    """Computes the metrics of the current model on the validation set"""

    model.eval()
    
    loss_valid = []
    target_valid = []
    pred_valid = []
    
    with torch.no_grad():
        for x, target, _ in tqdm(valid_loader, total=len(valid_loader), desc='Valid_' + str(valid_epoch)):
            x = x.to(device)
            target = target.to(device)
            
            output = model(x)
            loss = criterion(output, target)
            loss_valid.append(loss.item())
            
            target_valid.append(target.cpu().numpy())
            pred_valid.append(output.argmax(dim=1).cpu().numpy())
            
            del loss, x, target, output
    
    target_valid = np.concatenate(target_valid, axis=0)
    pred_valid = np.concatenate(pred_valid, axis=0)
    
    writer.add_scalar('Valid/loss', np.mean(loss_valid), valid_epoch)
    writer.add_scalar('F1_mean', f1_score(target_valid, pred_valid, average='macro'), valid_epoch)
    writer.add_scalar('Accuracy', (target_valid == pred_valid).sum() / target_valid.size, valid_epoch)


def gallery(images, plot_labels=False, label=None, max_images=10):
    """Displays images"""

    num_frames, _, _, num_channels = images.shape
    num_frames = min(num_frames, max_images)
    ff, axes = plt.subplots(1, num_frames,
                            figsize=(num_frames, 1),
                            subplot_kw={'xticks': [], 'yticks': []})
    
    for i in range(0, num_frames):
        if num_channels == 3:
            axes[i].imshow(np.squeeze(images[i]))
        else:
            axes[i].imshow(np.squeeze(images[i]), cmap='gray')
        if plot_labels:
            axes[i].set_title(label[i])
        
        plt.setp(axes[i].get_xticklabels(), visible=False)
        plt.setp(axes[i].get_yticklabels(), visible=False)
    
    ff.subplots_adjust(wspace=0.1)
    plt.show()

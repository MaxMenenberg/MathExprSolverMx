import torch
import numpy as np
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import PIL.Image as Image
import transforms as T
from engine import train_one_epoch, evaluate
import utils
from MathExpressionDataset import MEdataset
import os


def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)


# load a model pre-trained pre-trained on COCO
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

# replace the classifier with a new one, that has
# num_classes which is user-defined
num_classes = 109 #108 LaTeX symbols + the background/nothing

# get number of input features for the classifier
in_features = model.roi_heads.box_predictor.cls_score.in_features

# replace the pre-trained head with a new one
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)


trainDir = r'C:\Users\maxwe\Desktop\My Documents\MathExprSolverMx\MathExprSolverMx\AidaCalculusHandWrittenMathDataset\archive\train'
testDir = r'C:\Users\maxwe\Desktop\My Documents\MathExprSolverMx\MathExprSolverMx\AidaCalculusHandWrittenMathDataset\archive\test'


# train on the GPU or on the CPU, if a GPU is not available
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


# use our dataset and defined transformations
dataset = MEdataset(trainDir, get_transform(train=True))
dataset_test = MEdataset(testDir, get_transform(train=False))

# split the dataset in train and test set
indicesTrain = torch.randperm(len(dataset)).tolist()
indicesTest = torch.randperm(len(dataset_test)).tolist()
dataset = torch.utils.data.Subset(dataset, indicesTrain[:])
dataset_test = torch.utils.data.Subset(dataset_test, indicesTest[:])

# define training and validation data loaders
data_loader = torch.utils.data.DataLoader(
    dataset, batch_size=2, shuffle=True, num_workers=4,
    collate_fn=utils.collate_fn)

data_loader_test = torch.utils.data.DataLoader(
    dataset_test, batch_size=1, shuffle=False, num_workers=4,
    collate_fn=utils.collate_fn)

# move model to the right device
model.to(device)

# construct an optimizer
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.005,
                            momentum=0.9, weight_decay=0.0005)
# and a learning rate scheduler
lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                               step_size=3,
                                               gamma=0.1)

# let's train it for 10 epochs
num_epochs = 1

for epoch in range(num_epochs):
    # train for one epoch, printing every 10 iterations
    train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=10)
    # update the learning rate
    lr_scheduler.step()
    # evaluate on the test dataset
    evaluate(model, data_loader_test, device=device)

print("That's it!")

savePath = os.path.join(os.getcwd(), 'model1.pt')
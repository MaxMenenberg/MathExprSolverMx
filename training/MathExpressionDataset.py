import os
import numpy as np
import PIL.Image as Image
import json
import torch
    

class MEdataset(object):
    
    # Given a symbol value in the class label dictionary, get the corresponding
    # key which is the class label
    def getClassLabelFromSymbol(self, classLabelDict, symbol):
        
        for n in range(len(classLabelDict)):
            tempsymbol = classLabelDict[str(n+1)]
            if tempsymbol == symbol:
                return n+1
         
        raise ValueError('No class label found for this symbol.')
    
    def __init__(self, root, transforms):
        self.root = root
        self.transforms = transforms
        
        # Load all image and annotations files
        # and sort them to make sure their indices
        # are aligned
        self.imgs = list(sorted(os.listdir(os.path.join(root, 'images'))))
        self.annotations = list(sorted(os.listdir(os.path.join(root, 'annotations'))))
        with open(os.path.join(root, 'classLabels.json'), encoding = 'utf8') as f:
            self.classLabels = json.load(f)
        
        
    def __getitem__(self, idx):
        # Get the image and annotation file for the current index
        img_path = os.path.join(self.root, 'images', self.imgs[idx])
        annotation_path = os.path.join(self.root, 'annotations', self.annotations[idx])
        
        img = Image.open(img_path).convert("RGB")
        
        with open(annotation_path) as f:
            annotation = json.load(f)
        
        objNum = len(annotation['image_data']['visible_latex_chars'])
        boxes = []
        labels = []
        for n in range(objNum):
            xmin = annotation['image_data']['xmins_raw'][n]
            xmax = annotation['image_data']['xmaxs_raw'][n]
            ymin = annotation['image_data']['ymins_raw'][n]
            ymax = annotation['image_data']['ymaxs_raw'][n]
            boxes.append([xmin, ymin, xmax, ymax])
            labelSymbol = annotation['image_data']['visible_latex_chars'][n]
            labels.append(self.getClassLabelFromSymbol(self.classLabels, labelSymbol))
            
        # convert everything into a torch.Tensor
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.float32)
        image_id = torch.tensor([idx])
        
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        
        # suppose all instances are not crowd
        iscrowd = torch.zeros((objNum,), dtype=torch.int64)
        
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd
        
        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target
    
    def __len__(self):
        return len(self.imgs)
    
   
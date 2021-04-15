import torch
from MathExpressionDataset import MEdataset
 
rootDir = r'C:\Users\maxwe\Desktop\My Documents\MathExprSolverMx\MathExprSolverMx\whiteboardImages'
 
 
trainSet = MEdataset(rootDir, None)
img, trg = trainSet[11]
badIndices = []
for n in range(len(trainSet)):
    try:
        img, trg = trainSet[n]
        h = img.height-1
        w = img.width-1
        boxes = trg["boxes"]
        xValues = boxes[:,2]
        yValues = boxes[:,3]
        maxX = torch.max(xValues).item()
        maxY = torch.max(yValues).item()
        
        if maxX > w or maxY > h:
            print("Bounding Box Mismatch on index {}'th element".format(n))
            badIndices.append(n)
        else: 
            print("Index {} is good".format(n))
        
    except:
        print("Could not index {}'th element".format(n))

from MathExpressionDataset import MEdataset
 
rootDir = r'C:\Users\maxwe\Desktop\My Documents\MathExprSolverMx\MathExprSolverMx\AidaCalculusHandWrittenMathDataset\archive\train'
 
 
trainSet = MEdataset(rootDir, None)
img, trg = trainSet[4]
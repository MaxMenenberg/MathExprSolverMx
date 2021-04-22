import pickle
from MathExpressionMx import *
import MathExpressionProcessor as mep
import os

with open(os.path.join(os.getcwd(),r'testResources\detection2.bin'), 'rb') as f:
    detections = pickle.load(f)
    
symList = mep.processDetectionData(detections, 0.5)    
ME = MathExpression(symList)

for sym in ME.ExpressionSymbols:
    print(sym.symbol)
    
processedME = mep.processFrac(ME)
import pickle
from MathExpressionMx import *
import MathExpressionProcessor as mep
import os

with open(os.path.join(os.getcwd(),r'testResources\detection3.bin'), 'rb') as f:
    detections = pickle.load(f)
    
symList = mep.processDetectionData(detections, 0.5)    
ME = MathExpression(symList)

ME.fractionAnalysis()

for sym in ME.MathSymbolList:
    print(sym.symbol)
    for m in range(len(sym.numerators)):
        print('N' + str(sym.numerators[m]), end=' ')
    for m in range(len(sym.denominators)):
        print('D' + str(sym.denominators[m]), end=' ')
        
    print('')
    print('')
    
tempList = []
tempList.append(ME.MathSymbolList[1])
tempList.append(ME.MathSymbolList[4])

ME.sortSymbolListbySize(tempList)


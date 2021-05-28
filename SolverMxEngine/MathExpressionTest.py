import pickle
from MathExpressionMx import *
import MathExpressionProcessor as mep
import os

with open(os.path.join(os.getcwd(),r'testResources\detection5.bin'), 'rb') as f:
    detections = pickle.load(f)
    
symList = mep.processDetectionData(detections, 0.5)    
ME = MathExpression(symList)

ME.fractionAnalysis()
ME.exponentAnalysis()

# for sym in ME.MathSymbolList:
#     print(sym.symbol)
#     for m in range(len(sym.numerators)):
#         print('N' + str(sym.numerators[m]), end=' ')
#     for m in range(len(sym.denominators)):
#         print('D' + str(sym.denominators[m]), end=' ')
        
#     print('')
#     print('')
    
for sym in ME.MathSymbolList:
    print(sym.symbol)
    for m in range(len(sym.bases)):
        print('B' + str(sym.bases[m]), end=' ')
    for m in range(len(sym.exponents)):
        print('E' + str(sym.exponents[m]), end=' ')
        
    print('')
    print('')    

fourHeight = ME.MathSymbolList[1].height;
fourWidth = ME.MathSymbolList[1].width;
fourY = ME.MathSymbolList[1].center[1]
fourX = ME.MathSymbolList[1].center[0]

print('4: Height = {h} | Width = {w} | Ycent = {Y} | Xcent = {X}'.format(h=fourHeight,w=fourWidth, Y=fourY, X=fourX))

twoHeight = ME.MathSymbolList[2].height;
twoY = ME.MathSymbolList[2].center[1]
twoX = ME.MathSymbolList[2].center[0]

print('2: Height = {h} | Ycent = {Y} | Xcent = {X}'.format(h=twoHeight, Y=twoY, X=twoX))

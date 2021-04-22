import json
import numpy as np
import os
from MathExpressionMx import MathExpression, MathSymbol

# Process the output of the object detection model and returns a list of
# math symbols for the math expression constructor
def processDetectionData(detections, threshold):
        with open(os.path.join(os.getcwd(), 'classLabels.json'), encoding = 'utf8') as f:
            symbolMap = json.load(f)
            
        # Unpack the detection data
        boxes = np.round(detections[0]["boxes"].detach().numpy())
        labels = detections[0]["labels"].detach().numpy()
        scores = detections[0]["scores"].detach().numpy()
        
        MathSymbolList = []
        
        for n in range(len(scores)):
            if scores[n] > threshold:
                MathSymbolList.append(MathSymbol(boxes[n], symbolMap[str(labels[n])]))

        return MathSymbolList
    
    
# Take in a math expression with a one or mutiple fractions and recursivly 
# process them returning pairs of numerators and demoninatios
def processFrac(MathExpr):
    processedExpr = []
    fractionsDetected = False
    
    # Go through all symbols looking the largest fraction
    for n in range(len(MathExpr.ExpressionSymbols)):
        biggestFracSize = -1
        tempSym_n = MathExpr.ExpressionSymbols[n]
        if tempSym_n.symbol == '\\frac' and tempSym_n.width > biggestFracSize:
            fractionsDetected = True
            biggestFracSize = tempSym_n.width
            bigFrac = tempSym_n
            largestFracIndex = n
        
    if fractionsDetected == True:
        # Once we have found the largest fraction assign all elements involved
        # with this fraction to either the numerator or denominator
        tempNum = []
        tempDenom = []
        for n in range(len(MathExpr.ExpressionSymbols)):
            tempSym_n = MathExpr.ExpressionSymbols[n]
            if n == largestFracIndex:
                pass
            else:
                # is the symbol involved with the \frac
                if (tempSym_n.center[0] > bigFrac.box[0] and 
                    tempSym_n.center[0] < bigFrac.box[2]):
                    if tempSym_n.center[1] < bigFrac.center[1]:
                        tempNum.append(tempSym_n)
                    else:
                        tempDenom.append(tempSym_n)
                else:
                    processedExpr.append(tempSym_n)
                
                
        # Now that the numerator and demoniators symbols have been idenfied 
        # run the process fraction on them to identify more fractions
        proceExprNum = processFrac(MathExpression(tempNum))
        proceExprDemon = processFrac(MathExpression(tempDenom))
        processedExpr.append((proceExprNum, proceExprDemon))
    else:
        for n in range(len(MathExpr.ExpressionSymbols)):
            processedExpr.append(MathExpr.ExpressionSymbols[n])
    
    return processedExpr
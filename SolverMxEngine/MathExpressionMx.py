import os
import json
import numpy as np


class MathSymbol:
    
    def __init__(self, box, label):
        self.box = box
        self.symbol = label
        self.width = box[2] - box[0]
        self.height = box[3] - box[1]
        self.center = (np.mean((box[2], box[0])), np.mean((box[3], box[1]))) 
    
class MathExpression:
    
    def __init__(self, MathSymbolList):

        self.ExpressionSymbols = MathSymbolList
        self.unmapParens()
        
    # The object detection model does not do a good job and distinguishing
    # \\left( from \\right) so right from the start lets map all parens
    # to some unknown state $P$
    def unmapParens(self):
        for tempSym in self.ExpressionSymbols:
            if tempSym.symbol == '\\left(' or tempSym.symbol == '\\right)':
                tempSym.symbol = '$P$'
        
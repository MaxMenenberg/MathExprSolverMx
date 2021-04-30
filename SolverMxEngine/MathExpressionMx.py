import numpy as np


class MathSymbol:
    
    def __init__(self, box, label, index):
        self.box = box
        self.symbol = label
        self.index = index
        self.width = box[2] - box[0]
        self.height = box[3] - box[1]
        self.center = (np.mean((box[2], box[0])), np.mean((box[3], box[1]))) 
        self.isFrac = False
        self.fracIndex = -1
        self.numerators = []
        self.denominators = []
        self.bases = []
        self.exponents = []
        self.isRoot = []
        self.rootIndex = -1
        self.roots = []
    
class MathExpression:
    
    def __init__(self, MathSymbolList):

        self.MathSymbolList = MathSymbolList
        self.symbolCount = len(self.MathSymbolList)
        self.fracCount = 0;
        self.infixString = '';
        self.latexString = '';
        self.postfixString = '';
        self.unmapParens()
        
    # The object detection model does not do a good job and distinguishing
    # \\left( from \\right) so right from the start lets map all parens
    # to some unknown state $P$
    def unmapParens(self):
        for tempSym in self.MathSymbolList:
            if tempSym.symbol == '\\left(' or tempSym.symbol == '\\right)':
                tempSym.symbol = '$'
    
    # Check if a symbol exists in the math expression
    def symbolExist(self, symString):
        symExists = False;
        for n in range(self.symbolCount):
            if self.MathSymbolList[n].symbol == symString:
                symExists = True
                break
        return symExists
    
    # Count the number of occurences for a given symbel
    def symbolCount(self, symString):
        symCount = 0;
        if self.symbolExist(symString):
            for n in range(self.symbolCount):
                if self.MathSymbolList[n].symbol == symString:
                    symCount += 1
        return symCount
    
    # List is pass by reference so no return value needed          
    def sortSymbolListbySize(self, symList):
        # Just going to do a simple bubble sort
        for n in range(len(symList) - 1):
            for m in range(len(symList)-1):
                if symList[m].width < symList[m+1].width:
                    tempSym = symList[m]
                    symList[m] = symList[m+1]
                    symList[m+1] = tempSym
    
    # Identify which symbols are a part of what fractions
    def fractionAnalysis(self):
        if self.symbolExist(r'\frac') == False:
            return
        else:
            
            # Find all of the fractions
            fracList = []
            for n in range(self.symbolCount):
                if self.MathSymbolList[n].symbol == r'\frac':
                    fracList.append(self.MathSymbolList[n])
                    self.MathSymbolList[n].isFrac = True
            
            # Sort the fractions from largest to smallest
            self.sortSymbolListbySize(fracList)
            
            # For each fraction
            for n in range(len(fracList)):
                tempFrac = fracList[n]
                # Find it in the fraction list and assign it a fraction index
                for m in range(self.symbolCount):
                    if self.MathSymbolList[m].index == fracList[n].index:
                        self.MathSymbolList[m].fracIndex = n
                        break
                
                # Now append all symbols numerators field with the fraction 
                # index if they are above the fraction, or append to the 
                # denominators field if they are below the fraction. However
                # do not append to symbols above of below a previously 
                # processed fraction
                
                for m in range(self.symbolCount):
                    tempSym = self.MathSymbolList[m]
                    # We dont want to process the fraction we are analyzing
                    if tempSym.index != tempFrac.index:
                        
                        # If the symbol is over the fraction
                        if tempSym.center[0] > tempFrac.box[0] and tempSym.center[0] < tempFrac.box[2] and tempSym.center[1] < tempFrac.center[1]:
                            
                            # Now check if the symbol is above of below any previously processed fraction
                            readyToMark = True
                            for k in range(n):
                                # If the symbol is above a previouly marked fraction
                                if tempSym.center[0] > fracList[k].box[0] and tempSym.center[0] < fracList[k].box[2] and tempSym.center[1] < fracList[k].center[1]:
                                    readyToMark == False
                                # If the symbol is below a previously marked fraction
                                if tempSym.center[0] > fracList[k].box[0] and tempSym.center[0] < fracList[k].box[2] and tempSym.center[1] > fracList[k].center[1]:
                                    readyToMark == False
                                    
                            if readyToMark:
                                self.MathSymbolList[m].numerators.append(tempFrac.fracIndex)
                                
                        # If the symbol is under the fraction
                        elif tempSym.center[0] > tempFrac.box[0] and tempSym.center[0] < tempFrac.box[2] and tempSym.center[1] > tempFrac.center[1]:
                            
                            # Now check if the symbol is above of below any previously processed fraction
                            readyToMark = True
                            for k in range(n):
                                # If the symbol is above a previouly marked fraction
                                if tempSym.center[0] > fracList[k].box[0] and tempSym.center[0] < fracList[k].box[2] and tempSym.center[1] < fracList[k].center[1]:
                                    readyToMark == False
                                # If the symbol is below a previously marked fraction
                                if tempSym.center[0] > fracList[k].box[0] and tempSym.center[0] < fracList[k].box[2] and tempSym.center[1] > fracList[k].center[1]:
                                    readyToMark == False
                                    
                            if readyToMark:
                                self.MathSymbolList[m].denominators.append(tempFrac.fracIndex)
                        
                        # The symbol is not part of the fraction
                        else:
                            pass
            
        
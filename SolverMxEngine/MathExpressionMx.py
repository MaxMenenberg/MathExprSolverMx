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
        self.needsProcessing = True
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
        self.fracCount = 0
        self.exponCount = 0
        self.infixString = ''
        self.latexString = ''
        self.postfixString = ''
        self.unmapParens()
        self.exponentAnalysis()
        self.fractionAnalysis()
        
        
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
                    self.fractionCount += 1
            
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
                        
    # Identify which symboles are exponents and what their bases are
    def exponentAnalysis(self):
        alpha = 1.5  #Threshold for ratio of base to exponent
        beta = 0.6   #Threshold for normalized different of heights between base and exponent
        gamma = -1   #Threshold for normailzed difference in x-center between base and exponent
        # We also dont want the width of a possible exponent candidate to be large than the base,
        # this is to screen out a denominator thinking its fraction bar is an
        # exponent, but small fraction bars can be exponents
        
        
        
        # Operators cannot be a base of an exponential expression
        invalidBases = [r'\frac', '-', '+', '\\left(','\\right)', '*', '^']
        
        # For each symbols see if it has a neighbor that meets all of the 
        # exponent criteria. If so, mark them as exponent and base pairs
        
        baseIndex = 0;
        for n in range(self.symbolCount):
            
            if not (self.MathSymbolList[n].symbol in invalidBases):
                tempSymbol = self.MathSymbolList[n];
                
                for m in range(self.symbolCount):
                    if m != n: # Dont compare to self
                       tempSymbol2 = self.MathSymbolList[m]
                       
                       alphaCheck = tempSymbol.height/tempSymbol2.height > alpha
                       betaCheck = (tempSymbol.center[1] - tempSymbol2.center[1])/tempSymbol.height > beta
                       gammaCheck = ( (tempSymbol.center[0] - tempSymbol2.center[0])/tempSymbol.width > gamma 
                                     and (tempSymbol.center[0] - tempSymbol2.center[0]) < 0 )
                       widthCheck = tempSymbol.width > tempSymbol2.width;
                       
                       if alphaCheck and betaCheck and gammaCheck and widthCheck:
                           self.MathSymbolList[n].bases.append(baseIndex)
                           self.MathSymbolList[m].exponents.append(baseIndex)
                           baseIndex += 1
                           self.exponCount += 1
        
        # Now that the initial base exponent pairs have been found there might
        # still be other symbols part of exponents that didnt get caught because
        # the expression in the exponent is strucurally large. To try and find
        # the remaining exponent symbols we examine all symbols marked as 
        # exponents and see if they have neighbors that are likely also
        # part of the same expression in an exponent
        
        # Criteria: Symbol must be "near" the exponent and of a similar size
        delta = 2;
        epsilon = 0.75;
        for n in range(self.symbolCount):
            tempSymbol = self.MathSymbolList[n];
            if len(tempSymbol.exponents):
                tempH = tempSymbol.height;
                tempW = tempSymbol.width;
                tempX = tempSymbol.center[0]
                tempY = tempSymbol.center[1]
                for m in range(self.symbolCount):
                    tempSymbol2 = self.MathSymbolList[m];
                    if n != m and not any(item in tempSymbol.exponents for item in tempSymbol2.exponents):
                        temp2H = tempSymbol2.height;
                        temp2W = tempSymbol2.width;
                        temp2X = tempSymbol2.center[0]
                        temp2Y = tempSymbol2.center[1]
                        
                        xCheck = np.abs(tempX - temp2X)/tempW < delta
                        yCheck = np.abs(tempY - temp2Y)/tempH < delta
                        wCheck = tempW/temp2W > (1- epsilon) and tempW/temp2W < (1+epsilon)
                        hCheck = tempH/temp2H > (1- epsilon) and tempH/temp2H < (1+epsilon)
                        
                        if xCheck and yCheck and (wCheck or hCheck):
                            for k in range(len(tempSymbol.exponents)):
                                self.MathSymbolList[m].exponents.append(tempSymbol.exponents[k])
     
    # Process a simple epression. I.E. a list of symbols with no fractions
    # or exponents. A single line
    def processSimpleExpression(self, symbolList):
        # First sort the symbols from left to right
        
        for n in range(len(symbolList)):
            for m in range(len(symbolList)-1):
                if symbolList[m].center(0) > symbolList[m+1].center(0):
                    temp = symbolList[m]
                    symbolList[m] = symbolList[m+1]
                    symbolList[m+1] = temp
                    
        # Check if there are any unbalanced parentheses
        parenBalanceNeeded = False
        parenIndices = []
        for n in range(len(symbolList)):
            if symbolList[m].symbol == '$':
                parenBalanceNeeded = True
                parenIndices.append(n)
                
        if parenBalanceNeeded:
            parenBalance = False
            symbolList[parenIndices[0]].symbol = '\\left('
            symbolList[parenIndices[len(parenIndices)-1]].symbol = '\\right)'  
            
            if len(parenIndices) == 2:
                parenBalance = True
                
            # Hopefully we never have an odd number of parentheses
            if np.mod(len(parenIndices), 2) == 1:
                endSym = symbolList[len(symbolList)-1]
                symbolList.append(MathSymbol(endSym.box, '\\right)', endSym.index))
            
            # Create some initial state for the other unassigned parentheses
            for n in range(1, len(parenIndices)-1, 1):
                    if np.mod(n, 2) == 1:
                        symbolList[parenIndices[n]].symbol == '\\right)'
                    else:
                        symbolList[parenIndices[n]].symbol == '\\left('
                    
            while(parenBalance == False):
                
               # Check the following set of rules and only if all rules are met
               # can we set parenBalance == True
               
               # Check #1: There must be equal number of \\right) to \\left(
               check1 = False
               leftCount = 0
               rightCount = 0
               for n in range(len(symbolList)):
                   if symbolList[n].symbol == '\\left(':
                       leftCount += 1
                   if symbolList[n].symbol == '\\right)':
                       rightCount += 1
                       
               if leftCount == rightCount:
                   check1 = True;
                
                # Check #2: There cant be the sequence ()
               check2 = True
               for n in range(len(symbolList)-1):
                    if symbolList[n].symbol == '\\left(' and symbolList[n+1].symbol == '\\right)':
                        check2 = False
               
               # Check #3: There can't be a binary operator before a )
               binOperators = ['-', '+', '*', '^', '/']
               check3 = True
               for n in range(len(symbolList)-1):
                    if symbolList[n].symbol in binOperators and symbolList[n+1].symbol == '\\right)':
                        check3 = False
                
               if check1 and check2 and check3:
                    parenBalance = True
                
               # If corrections need to be made
               if parenBalance == False:
                   
                   if check2 == False:
                       for n in range(len(symbolList)-1):
                           if symbolList[n].symbol == '\\left(' and symbolList[n+1].symbol == '\\right)':
                               symbolList[n].symbol == '\\right)'
                               symbolList[n+1].symbol == '\\left('
                               
                   if check3 == False:
                       for n in range(len(symbolList)-1):
                           if symbolList[n].symbol in binOperators and symbolList[n+1].symbol == '\\right)':
                               symbolList[n+1].symbol == '\\left('
                               
                               # Then find the left parenthese to the left of this symbol we just corrected and
                               # change it to a \\right. If we dont find any to the left, search to the right
                               
                               foundLeft = False
                               for m in range(n, 0, -1):
                                   if symbolList[m].symbol == '\\left(':
                                       symbolList[m].symbol == '\\right)'
                                       foundLeft = True
                               if not foundLeft:
                                     for m in range(n+2, len(symbolList)-1, 1):
                                         if symbolList[m].symbol == '\\left(':
                                             symbolList[m].symbol == '\\right)'
                                             foundLeft = True
                               
            # Now that the parentheses are balanced
            newSymbolString = '';
            for n in range(len(symbolList)):
                newSymbolString += symbolList[m].symbol
                
            newSymbolBox = []
            newSymbolBox.append(symbolList[0].box[0])  # xmin
            newSymbolBox.append(symbolList[0].box[1])  # ymin
            newSymbolBox.append(symbolList[-1].box[2]) # xmax
            newSymbolBox.append(symbolList[0].box[3])  # ymax
            
            return MathSymbol(newSymbolBox, newSymbolString, symbolList[0].index)
                               
    def createInfixString(self):
        
        # Process exponent sub expressions if any
        if self.exponCount > 0:
            highestIndex = self.exponCount - 1
            
            for n in range(highestIndex, -1, -1):
                tempExSyms = [];
                
                for m in range(self.symbolCount):
                    tempSymbol = self.MathSymbolList[m]
                    if n in tempSymbol.exponents:
                        tempExSyms.append(self.MathSymbolList[m])
                        
                # Now check if there are any fractions in the subexpression
                for m in range(len(tempExSyms)):
                    if tempExSyms[m].symbol == r'\frac':
                        tempFracIndex = tempExSyms[m].fracIndex
                        numerator = []
                        denominator = []
                        for k in range(len(tempExSyms)):
                            if tempFracIndex in tempExSyms[k].numerators:
                                numerator.append(tempExSyms[k])
                            if tempFracIndex in tempExSyms[k].denominators:
                                denominator.append(tempExSyms[k])
                        
                        pass
                    pass
                pass
                    
                        
                               
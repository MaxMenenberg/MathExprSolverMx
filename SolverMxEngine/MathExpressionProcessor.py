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
        
        symCount = 0
        for n in range(len(scores)):
            if scores[n] > threshold:
                MathSymbolList.append(MathSymbol(boxes[n], symbolMap[str(labels[n])], symCount))
                symCount += 1

        return MathSymbolList
    

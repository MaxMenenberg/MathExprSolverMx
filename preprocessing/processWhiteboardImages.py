import os
import json
import xml.etree.ElementTree as ET
import random
import string
from ast import literal_eval

def getClassLabelFromSymbol(classLabelDict, symbol):
    
    for n in range(len(classLabelDict)):
        tempsymbol = classLabelDict[str(n+1)]
        if tempsymbol == symbol:
            return n+1
     
    raise ValueError('No class label found for this symbol.')

whiteboardImageDir = r'C:\Users\maxwe\Desktop\My Documents\MathExprSolverMx\MathExprSolverMx\whiteboardImages'
wbFiles = os.listdir(whiteboardImageDir)
tempXML = os.path.join(whiteboardImageDir, wbFiles[2])
tree = ET.parse(tempXML)

with open(os.path.join(os.getcwd(), 'classLabels.json'), encoding = 'utf8') as f:
            classLabels = json.load(f)

for n in range(len(wbFiles)):
    if wbFiles[n][-4:] == '.xml':
        tempXML = os.path.join(whiteboardImageDir, wbFiles[n])
        tree = ET.parse(tempXML)
        root = tree.getroot();
        
        jsonDict = {}
        
        # Get the file name and uuid
        temp = root.findall('filename')
        jsonDict['filename'] = temp[0].text
        jsonDict['uuid'] = temp[0].text[:-4]
        
        # Get the image dimensions
        temp = root.findall('size')
        width = int(temp[0].find('width').text)
        height = int(temp[0].find('height').text)
        
        # Get the bounding box coordinates and LaTeX characters
        imageDataDict = {}
        imageDataDict['depth'] = 4;
        visLatexChars = []
        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        
        detectedObjs = root.findall('object')
        for obj in detectedObjs:
            visLatexChars.append(literal_eval("'%s'" % obj.find('name').text))
            xmins.append(int(obj.find('bndbox').find('xmin').text))
            xmaxs.append(int(obj.find('bndbox').find('xmax').text))
            ymins.append(int(obj.find('bndbox').find('ymin').text))
            ymaxs.append(int(obj.find('bndbox').find('ymax').text))
            
        imageDataDict['visible_latex_chars'] = visLatexChars
        imageDataDict['xmaxs_raw'] = xmaxs
        imageDataDict['xmins_raw'] = xmins
        imageDataDict['ymaxs_raw'] = ymaxs
        imageDataDict['ymins_raw'] = ymins
        
        jsonDict['image_data'] = imageDataDict
        
        tempJsonFileName = wbFiles[n][:-4] + '.json'
        tempJsonFile = os.path.join(whiteboardImageDir, tempJsonFileName)
        
        with open(tempJsonFile, 'w') as tempf:
            json.dump(jsonDict, tempf)
            print('Saving {0} metadata file. {1}% complete'.format(tempJsonFileName, n*100/len(wbFiles)))
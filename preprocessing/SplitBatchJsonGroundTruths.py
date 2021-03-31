import json
import ast
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from IPython.display import display


batchNum = 10
batchDir = os.path.join(
    os.path.dirname(os.getcwd()), 
    r'AidaCalculusHandWrittenMathDataset\archive\batch_'+str(batchNum))

imageDir = os.path.join(batchDir, 'background_images')
jsonDir = os.path.join(batchDir, 'JSON')
jsonFile = os.path.join(jsonDir, 'kaggle_data_'+str(batchNum)+'.json')
annotationDir = os.path.join(batchDir, 'annotations')

if os.path.isdir(annotationDir) == False:
    os.mkdir(annotationDir)

with open(jsonFile) as f:
    data = json.load(f)
    
for n in range(len(data)):
    tempMetaData = data[n]
    tempJsonFileName = os.path.join(annotationDir,
                                    tempMetaData['uuid'] + '.json')
    with open(tempJsonFileName, 'w') as tempf:
        json.dump(tempMetaData, tempf)
    print('Saving {0} metadata file. {1}% complete'.format(tempJsonFileName, n*100/len(data)))
    
    
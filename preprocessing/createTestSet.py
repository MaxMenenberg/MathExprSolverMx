import os
import random as rnd


trainDirImage = batchDir = os.path.join(
    os.path.dirname(os.getcwd()), 
    r'AidaCalculusHandWrittenMathDataset\archive\train\images')

trainDirAnnotations = batchDir = os.path.join(
    os.path.dirname(os.getcwd()), 
    r'AidaCalculusHandWrittenMathDataset\archive\train\annotations')

testDirImage = batchDir = os.path.join(
    os.path.dirname(os.getcwd()), 
    r'AidaCalculusHandWrittenMathDataset\archive\test\images')

testDirAnnotations = batchDir = os.path.join(
    os.path.dirname(os.getcwd()), 
    r'AidaCalculusHandWrittenMathDataset\archive\test\annotations')

imageNum = 100000;
testNum = 523;
imageFiles = os.listdir(trainDirImage)

for n in range(testNum):
    # Find a random file
    randomIndex = rnd.randint(0, imageNum-1002)
    tempImageName = imageFiles[randomIndex]
    tempAnnotationName = tempImageName[:-4] + '.json'
    
    # The move the corresponding image and annotation file to the 
    # test directory
    tempImageFile = os.path.join(trainDirImage, tempImageName)
    tempAnnotationFile = os.path.join(trainDirAnnotations, tempAnnotationName)

    os.replace(tempImageFile, os.path.join(testDirImage, tempImageName))
    os.replace(tempAnnotationFile, os.path.join(testDirAnnotations, tempAnnotationName))
    
    print('Moving {0} files. {1}% complete'.format(tempImageName, n*100/testNum))
    
    
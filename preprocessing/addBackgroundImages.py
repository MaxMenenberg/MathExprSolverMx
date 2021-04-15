import os
import random
import string

def genRandomString(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def createEmptyJsonFile(filePath):
    f = open(filePath, 'x')
    f.close()

baseDir = os.path.dirname(os.getcwd())
bkgdImgDir = os.path.join(baseDir, r'BackgroundImages\test2017\test2017')
trainImgDir = os.path.join(baseDir, r'AidaCalculusHandWrittenMathDataset\archive\train\images')
trainAnnoDir = os.path.join(baseDir, r'AidaCalculusHandWrittenMathDataset\archive\train\annotations')
bkgdImgFiles = os.listdir(bkgdImgDir)

fileSuffixImg = '-bkgrdImg.jpg'
fileSuffixJson = '-bkgrdImg.json'
Ns = 10000
Ne = 30000


for n in range(Ns, Ne):
    
    # Location to the source background image
    srcImage = os.path.join(bkgdImgDir, bkgdImgFiles[n])
    
    # Make a new image/annotation file name pair
    randomPrefix = genRandomString(20)
    newImageName = randomPrefix + fileSuffixImg
    newAnnotationName = randomPrefix + fileSuffixJson
    
    # Make the destination of for new image and annotation file
    destImage = os.path.join(trainImgDir, newImageName)
    destJson = os.path.join(trainAnnoDir, newAnnotationName)
    
    # Move the image
    os.rename(srcImage, destImage)
    
    # Create the json
    createEmptyJsonFile(destJson)
    
    print('Moved {0} files. {1}% complete'.format(bkgdImgFiles[n], n*100/(Ne-Ns)))
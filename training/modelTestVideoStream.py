import torch
import numpy as np
import torchvision
import os
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import PIL.Image as Image
from PIL import ImageDraw
import transforms
import json
from IPython.display import display
import cv2

to_tensor = transforms.ToTensor()
def frame2Tensor(frame):
    image = to_tensor(frame,0)[0] #Needs 2nd "target" argument for some reason
    image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
    image = image.cuda() # Since we are using CUDA gpu
    return image

def add_text_border(draw_obj, text, xmin, ymin):
    """
    Add a thin black border around the text, helps with visualization. Modifies the draw object in place.
    
    Parameters
    ----------
    draw_obj : PIL.ImageDraw.ImageDraw
        The draw object.
    font : PIL.ImageFont.FreeTypeFont
        The ImageFont to add a border to.
    text : str
        The precise text being outlined, generally the label.
    xmin, ymin: int
        The xmin and ymin for the starting point of the text. (Top-Left)
    
    Returns
    ----------
    None
    """
    # Add a thin border.
    draw_obj.text((xmin-2, ymin), text, fill="black")
    draw_obj.text((xmin+2, ymin), text, fill="black")
    draw_obj.text((xmin, ymin-2), text, fill="black")
    draw_obj.text((xmin, ymin+2), text, fill="black")


def draw_bounding_boxes_on_image(img, xmins, ymins, xmaxs, ymaxs, labels,scores, scoreLim):
    """
    Draws and labels bounding boxes on source image using ground truth lists of details pertaining to the source image. Modifies the source image in place.
    
    Parameters
    ----------
    img : PIL.Image.Image
        The source image.
    xmins, ymins, xmaxs, ymaxs : list
        A list of the respectful coordinates for the image
    labels : list
        A list of labels for each character to be drawn.

    Returns
    ----------
    None
    """
    draw_obj = ImageDraw.Draw(img)
    for xmin, ymin, xmax, ymax, label, score in zip(xmins, ymins, xmaxs, ymaxs, labels,scores):
        if score > scoreLim:
            draw_obj.rectangle([xmin, ymin, xmax, ymax], width=3, outline=(255,0,0))
            text = str(label)
            #add_text_border(draw_obj, text, xmin, ymin)
            draw_obj.text((xmin, ymin), text, fill = (0,0,255), stroke_width=5)
            
video_capture = cv2.VideoCapture(0)

modelFile = r'C:\Users\maxwe\Desktop\My Documents\MathExprSolverMx\MathExprSolverMx\training\mathRecognizerMx_4epochw20kBgrd.pt'
#modelFile = r'C:\Users\maxwe\Desktop\My Documents\MathExprSolverMx\MathExprSolverMx\training\mathRecognizerMx_1epoch.pt'

with open(os.path.join(os.getcwd(), 'classLabels.json'), encoding = 'utf8') as f:
    classLabels = json.load(f)
    
# Load the model
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
num_classes = 109 #108 LaTeX symbols + the background/nothing

in_features = model.roi_heads.box_predictor.cls_score.in_features

# replace the pre-trained head with a new one
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

# Apply the new model file
model.load_state_dict(torch.load(modelFile))
model.eval()

# train on the GPU or on the CPU, if a GPU is not available
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# move model to the right device
model.to(device)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    
    
    PIL_image = Image.fromarray(np.uint8(frame)).convert('RGB')
    try: 
        imageTensor = frame2Tensor(PIL_image)
        detections = model(imageTensor)
        boxes = np.round(detections[0]["boxes"].detach().cpu().numpy())
        labels = detections[0]["labels"].detach().cpu().numpy()
        scores = detections[0]["scores"].detach().cpu().numpy()
        labelSymbols = [];
        for n in range(len(labels)):
            labelSymbols.append(classLabels[str(labels[n])])
        draw_bounding_boxes_on_image(PIL_image, boxes[:,0],  boxes[:,1], boxes[:,2],  boxes[:,3], labelSymbols ,scores,scoreLim=0.75)
    except:
        print('Error Processing Frame')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    processedFrame = np.array(PIL_image) 
    cv2.imshow('Video', processedFrame)
    
# When everything done, release the capture
video_capture.release()
cv2.destroyAllWindows()
torch.cuda.empty_cache()
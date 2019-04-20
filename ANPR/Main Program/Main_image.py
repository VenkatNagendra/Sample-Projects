import cv2
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import DetectChars
import DetectPlates
from PIL import Image
import Plate


SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

def main(image,showSteps):

    CnnClassifier = DetectChars.loadCNNClassifier()         
    showSteps = showSteps

    if CnnClassifier == False:                               
        print("\nerror: CNN traning was not successful\n")               
        return                                                          

    imgOriginalScene  = cv2.imread(image)               
    
    h, w = imgOriginalScene.shape[:2]
    imgOriginalScene = cv2.resize(imgOriginalScene, (0, 0), fx = 1.4, fy = 1.4,interpolation=cv2.INTER_CUBIC)
    
    if imgOriginalScene is None:                            
        print("\nerror: image not read from file \n\n")      
        os.system("pause")                                  
        return                                              

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           
                                                                                        


    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        

    if showSteps == True:
        Image.fromarray(imgOriginalScene,'RGB').show() 
        

    if len(listOfPossiblePlates) == 0:                          
        print("\nno license plates were detected\n")             
        response = ' '
        return response,imgOriginalScene
    else:                                                       
          
        listOfPossiblePlates.sort(key = lambda Plate: len(Plate.strChars), reverse = True)

        licPlate = listOfPossiblePlates[0]

        if showSteps == True:
            Image.fromarray(licPlate.imgPlate).show()    
            
        if len(licPlate.strChars) == 0:                     
            print("\nno characters were detected\n\n")       
            return ' ',imgOriginalScene                                       
        

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             
        
        if showSteps == True:
            writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)           

            Image.fromarray(imgOriginalScene).show()               

            cv2.imwrite("imgOriginalScene.png", imgOriginalScene)           
            
    return licPlate.strChars,licPlate,imgOriginalScene

def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)



def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      
    fltFontScale = float(plateHeight) / 30.0                    
    intFontThickness = int(round(fltFontScale * 1.5))           

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        

            
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)         

    if intPlateCenterY < (sceneHeight * 0.75):                                                  
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      
    else:                                                                                       
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      
    

    textSizeWidth, textSizeHeight = textSize                

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          
     
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)



if __name__ == '__main__':
    main('images.jpg',True)
    

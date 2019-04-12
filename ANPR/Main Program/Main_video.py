import os
import time
import videosplit_sklearn
import Main_image
import cv2
from PIL import Image



if __name__ == '__main__':
    name = str(input('Enter the name of the video: '))
    (vdolength,totalFrames) = videosplit_sklearn.Launch(name)
	
    os.chdir('data')

    result = {}
    result_plate = {}
    result_imag = {}
    
    startTime = time.time()
    for f in os.listdir():
        
        pred, img , orgimg = Main_image.main(f,False)
        if pred in result.keys():
            result[pred] = result[pred] + 1
        elif pred != ' ':
            result[pred] = 1
            result_plate[pred] = img
            result_imag[pred] = orgimg

   
    endTime = time.time()
    
    l = {x: y for y, x in result.items()}
    r = list(sorted(l.keys()))
    index = r[len(r) - 1]
    plate = l[index]
    img = result_plate[plate]
    orgimg = result_imag[plate]
    executionTime = "{0:.2f}".format(endTime - startTime)
    print('The name plate is :', plate, ' frequency is: ', result[plate])
    
    try:
        Main_image.writeLicensePlateCharsOnImage(orgimg, img)
        Image.fromarray(orgimg).show()
    except:
        print("Problem in displaying license plate")
    print('execution time is : ' + executionTime)
    
    os.chdir('..')
    licensePlatePath = './LicensePlates/'+name.split('.')[0]+'.jpg'
    try:
        cv2.imwrite(licensePlatePath,img.imgPlate)
    except:
        print("Problem in writing license plate image")
        
    

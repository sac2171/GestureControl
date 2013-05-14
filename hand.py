import cv2 as Cv
import numpy as np
import face as Face


#For use with is skin detector
#MAX_HSV = (187,140,238)
#MIN_HSV = (120,30,0)
MAX_HSV = (166,91,139)
MIN_HSV = (120,30,47)


MAX_RGB = (129,163,140)
MIN_RGB = (61,30,64)



CV_FILLED = -1

camera_number = 0
DETECTOR_TYPE_HAAR_DEF_FRONT = 1;
DETECTOR_TYPE_HAAR_FRONT = 2;
DETECTOR_TYPE_LPB_FRONT = 0;

ESCAPE_KEY_CODE = 27
blur_constant = 4

SMOOTH_VARIABLES = (8,8)


def filter_skin(im):
    im = Cv.cvtColor(im,Cv.COLOR_BGR2HSV)
    #im = Cv.cvtColor(im,Cv.COLOR_BGR2RGB)
    
    filter_im = Cv.inRange(im,MIN_HSV, MAX_HSV )
    #filter_im = Cv.inRange(im,MIN_RGB, MAX_RGB)
    return filter_im

def getLargestCountour(im):
    #Get all contours
    contours, hierarchy = Cv.findContours(im,Cv.RETR_LIST,Cv.CHAIN_APPROX_NONE)
    
    
    smallContours = []
    for index in range(len(contours)):
        area = Cv.contourArea(contours[index])
        if area < 5e3: smallContours.append(index)
        smallContours.sort(reverse=True)        
    for index in smallContours: contours.pop(index)
    
    
    if len(contours) != 0:
        return contours
    else: 
        0 


def remove_face(im, bb):
    print ''
    #im.CV
    
def remove_faces(im,bb1,bb2,bb3):
    remove_face(im, bb1)
    remove_face(im, bb2)
    remove_face(im, bb3)
    

if __name__ == '__main__':
    
    camera = Cv.VideoCapture(camera_number)
    
    #Create detectors for each face type
    d1 = Face.FaceDetector(DETECTOR_TYPE_LPB_FRONT)
    d2= Face.FaceDetector(DETECTOR_TYPE_HAAR_FRONT)
    d3= Face.FaceDetector(DETECTOR_TYPE_LPB_FRONT)
    
    faces = []
    
    face_detected = False
    
    if camera.isOpened():
        rc, orig_frame = camera.read()
    else:
        rc = False
    
    while rc:
        
        #Flip so that hand will move in correct direction
        im = Cv.flip(orig_frame, 1)
        #im = Cv.blur(blur_constant)
        
        faces1 = d1.detect_faces(im)
        faces2 = d2.detect_faces(im)
        faces3 = d3.detect_faces(im)
        bb1,bb2,bbb3, = (0,0,0,0),(0,0,0,0),(0,0,0,0)
        if len(faces1) > 0:
            bb1  = faces1[0]
            (x,y,w,h) = faces1[0]
            Cv.rectangle(im, (x,y), (x+w,y+h), 255, CV_FILLED)
            
        if len(faces2) > 0:
            bb2  = faces2[0]
            (x,y,w,h) = faces2[0]
            Cv.rectangle(im, (x,y), (x+w,y+h), 180, CV_FILLED)
            #region_of_interest = im[x:x+w, y,y+h]
            #hsv = Cv.cvtColor(region_of_interest, Cv.COLOR_BGR2HSV)
            #Cv.putText(hsv.__str__())  
        
        if len(faces3) > 0:
            bb3  = faces3[0]
            (x,y,w,h) = faces3[0]
            Cv.rectangle(im, (x,y), (x+w,y+h), CV_FILLED)
                    
        #im = Cv.blur(im, (9,9))    
        im = filter_skin(im)
        
        
        #countours = getLargestCountour(im)
        #
        
        #Cv.
        #Cv.putText()
        
        #contours, hierarchy = cv2.findContours(filter_,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        
        
        
        
        Cv.imshow('Hand', im)
        
        rc, orig_frame = camera.read()
        
        key = Cv.waitKey(20)    
        if key == ESCAPE_KEY_CODE:
            break
    
import cv2 as Cv
import numpy as np
import face as Face


#For use with is skin detector
MAX_HSV = (187,140,238)
MIN_HSV = (120,30,0)



camera_number = 0
DETECTOR_TYPE_HAAR_DEF_FRONT = 1;
DETECTOR_TYPE_HAAR_FRONT = 2;
DETECTOR_TYPE_LPB_FRONT = 0;

ESCAPE_KEY_CODE = 27
blur_constant = 4

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
        
        if len(faces1) > 0:
            (x,y,w,h) = faces1[0]
            Cv.rectangle(im, (x,y), (x+w,y+h), 255)
            
        if len(faces2) > 0:
            (x,y,w,h) = faces2[0]
            Cv.rectangle(im, (x,y), (x+w,y+h), 180)
            #region_of_interest = im[x:x+w, y,y+h]
            #hsv = Cv.cvtColor(region_of_interest, Cv.COLOR_BGR2HSV)
            #Cv.putText(hsv.__str__())  
        
        if len(faces3) > 0:
            (x,y,w,h) = faces3[0]
            Cv.rectangle(im, (x,y), (x+w,y+h), 0)
        
        
        
        #Cv.
        #Cv.putText()
        
        #contours, hierarchy = cv2.findContours(filter_,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        
        
        
        
        Cv.imshow('Hand', im)
        
        rc, orig_frame = camera.read()
        
        key = Cv.waitKey(20)    
        if key == ESCAPE_KEY_CODE:
            break
    
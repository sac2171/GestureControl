import cv2
import numpy
 
HAAR_CASCADE_PATH = "haarcascade_frontalface_default.xml"
CAMERA_INDEX = 0

def detect_faces(image):
    faces = []
    cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    detected = cascade.detectMultiScale(image, 1.2, 2, cv2.CASCADE_DO_CANNY_PRUNING, (100,100))
    #print type(detected)
    #print detected
    #detected = cv2.CascadeClassifier.detectMultiScale(image, 1.2, 2, cv2.CASCADE_DO_CANNY_PRUNING, (100,100))
    if type(detected) is numpy.ndarray:
        for (x,y,w,h)in detected:
            faces.append((x,y,w,h))
    return faces

 

#cv2.namedWindow("Video", cv2.CV_WINDOW_AUTOSIZE)

capture = cv2.VideoCapture(0)
#storage = cv.CreateMemStorage()
#cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
faces = []

if capture.isOpened():
    returnValue, image = capture.read()
else:
    returnValue = False;
i = 0
while returnValue:
    
    framegray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
    # Only run the Detection algorithm every 5 frames to improve performance
    
    #if i%5==0:
    faces = detect_faces(image)
        #print 'huh?'


    for (x,y,w,h) in faces:                     
        cv2.rectangle(framegray, (x,y), (x+w,y+h), 255)  
        print 'detected' 
    #cv2.rectangle(framegray, (320,158), (320+124,158+124), 255)
    #huh 
    
    cv2.imshow("test", framegray)
    returnValue, image = capture.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    i += 1
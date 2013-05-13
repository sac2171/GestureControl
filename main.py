import cv2
import numpy as np
import utility
import face, face2
import sys

set_mouse_position = lambda x: x
vc = cv2.VideoCapture(0)

height = 480
width = 640

H = 187
S = 140
V = 238

lowH = 120
lowS = 30
lowV = 0

iterations = 0
x_mid, y_mid = 0, 0
if sys.platform == 'win32':
    import win32api
    x_mid = win32api.GetSystemMetrics(0) / 2
    y_mid = win32api.GetSystemMetrics(1) / 2
    set_mouse_position = win32api.SetCursorPosition
elif sys.platform == 'darwin':
    import Quartz.CoreGraphics, Quartz
    main_monitor = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
    x_mid = main_monitor.size.width / 2
    y_mid = main_monitor.size.height / 2
    set_mouse_position = Quartz.CoreGraphics.CGWarpMouseCursorPosition

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

face_detector = face.FaceDetector(0)
while rval:
    faces = face_detector.detect_faces(frame)
    newHSV = np.zeros((height,width),np.uint8)
    framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    justSkin = cv2.inRange(framegray,(lowH,lowS,lowV),(H,S,V))
    cv2.imshow("skin", justSkin)
    h1, w1 = framegray.shape[:2]
    newFrame = np.zeros((h1,w1),np.uint8)
    #justSkin = cv2.flip(justSkin,1)
    contours, hierarchy = cv2.findContours(justSkin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    max = 0
    max_index = 0
    for x in range(len(contours)):
        cnt_len = cv2.contourArea(contours[x])
        if cnt_len > max:
            max = cnt_len
            max_index = x
    cv2.drawContours(newFrame,contours[max_index],-1,255,-1)
    for face in faces:
        x, y = face[0], face[1]
        w, h = face[2], face[3]
        cv2.rectangle(newFrame, (x, y), (x+w, y+h), 255)

    mu = cv2.moments(contours[max_index],False)
    centerOfMass = (int( mu['m10']/mu['m00']),int( mu['m01']/mu['m00']))
    cv2.circle(newFrame, centerOfMass, 2, (140,140,140), 1 );
    #cv2.imshow("preview", framegray)
    #cv2.imshow("output",newFrame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    #if key == 32:
    #    print "ScreenShot Taken"
    #    cv2.imwrite(utility.rand_string()+".jpg",framegray )
    #if key == 27: # exit on ESC
    #    break
    

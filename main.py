import cv2
import numpy as np
import utility
#import win32api, win32con


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

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
while rval:
    iterations = iterations +1
    print iterations
    rectangles = cascade.detectMultiScale(frame)
    newHSV = np.zeros((height,width),np.uint8)
    framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    justSkin = cv2.inRange(framegray,(lowH,lowS,lowV),(H,S,V))
    #ret,justSkin = cv2.threshold(justSkin, 0,255,0)
    h1, w1 = framegray.shape[:2]
    newFrame = np.zeros((h1,w1),np.uint8)
    justSkin = cv2.flip(justSkin,1)
    contours, hierarchy = cv2.findContours(justSkin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    max = 0
    max_index = 0
    for x in range(len(contours)):
        cnt_len = cv2.contourArea(contours[x])
        if cnt_len > max:
            max = cnt_len
            max_index = x
    print len(contours)
    cv2.drawContours(newFrame,contours[max_index],-1,255,-1)
    if not len(rectangles) == 0:
        rectangle = rectangles[0]
        cv2.rectangle(newFrame, (rectangle[0], rectangle[1]), (rectangle[0]+rectangle[2], rectangle[1]+rectangle[3]), (255,0,0))
    mu = cv2.moments(contours[max_index],False)
    centerOfMass = (int( mu['m10']/mu['m00']),int( mu['m01']/mu['m00']))
    #mu.get_m10()
    cv2.circle(newFrame, centerOfMass, 2, (140,140,140), 1 );
    #print win32con
    #print centerOfMass
    #win32api.SetCursorPos(centerOfMass)
    #cv2.imshow("preview", framegray)
    cv2.imshow("output",newFrame)
    print len(contours)
    #cv2.findContours()
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 32:
        print "ScreenShot Taken"
        cv2.imwrite(utility.rand_string()+".jpg",framegray )
    if key == 27: # exit on ESC
        break
    

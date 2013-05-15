import cv2
import numpy as np
import utility
#import win32api, win32con

#cv2.namedWindow("preview")
#cv2.namedWindow("output")
vc = cv2.VideoCapture(0)
height = 480
width = 640


MAX_HSV = (166,91,139)
MIN_HSV = (120,30,47)

H = 166
S = 91
V = 139

lowH = 120
lowS = 30
lowV = 47

# H = 187
# S = 140
# V = 238
# 
# lowH = 120
# lowS = 30
# lowV = 0


def trackChange(type):
    if type =="H":
        def trackChange(newVal):
            global H
            H = newVal
        return trackChange
    if type =="S":
        def trackChange(newVal):
            global S
            S = newVal
        return trackChange
    if type =="V":
        def trackChange(newVal):
            global V
            V = newVal
        return trackChange

def trackChangeL(type):
    if type =="H":
        def trackChange(newVal):
            global lowH
            lowH = newVal
        return trackChange
    if type =="S":
        def trackChange(newVal):
            global lowS
            lowS = newVal
        return trackChange
    if type =="V":
        def trackChange(newVal):
            global lowV
            lowV = newVal
        return trackChange

iter = 0
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

iterations = 0
while rval and iterations < 150:
    rval, frame = vc.read()
    cv2.rectangle(frame, (600,200), (800,400), 255)
    cv2.imshow("sup",frame)
    iterations += 1

hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
boxed_image = hsv[200:399,600:799]
hsv = cv2.split(boxed_image)
h = hsv[0]
s = hsv[1]
v = hsv[2]
min_hsv = (int(h.mean()-h.std()), int(s.mean()-s.std()), int(v.mean()-v.std()))
max_hsv = (int(h.mean()+h.std()), int(s.mean()+s.std()), int(v.mean()+v.std()))
H = max_hsv[0]
S = max_hsv[1]
V = max_hsv[2]
lowH = min_hsv[0]
lowS = min_hsv[1]
lowV = min_hsv[2]

while rval:
    iter = iter+1
#     print iter
    cv2.createTrackbar("HL", "output", lowH, 180, trackChangeL("H"))
    cv2.createTrackbar("SL", "output", lowS, 255, trackChangeL("S"))
    cv2.createTrackbar("VL", "output", lowV, 255, trackChangeL("V"))
    cv2.createTrackbar("H", "output", H, 180, trackChange("H"))
    cv2.createTrackbar("S", "output", S, 255, trackChange("S"))
    cv2.createTrackbar("V", "output", V, 255, trackChange("V"))
    #newHSV = np.zeros((height,width),np.uint8)
    #framegray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #ramegray = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
    #framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    justSkin = cv2.inRange(framegray,(lowH,lowS,lowV),(H,S,V))
    #justSkin = cv2.inRange(framegray,lowH,H)
    #ret,justSkin = cv2.threshold(justSkin, 0,255,0)
    #h1, w1 = framegray.shape[:2]
    #newFrame = np.zeros((h1,w1),np.uint8)
    #justSkin = cv2.flip(justSkin,1)
    #contours, hierarchy = cv2.findContours(justSkin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #max = 0
    #max_index = 0
#      for x in range(len(contours)):
#          cnt_len = cv2.contourArea(contours[x])
#          if cnt_len > max:
#              max = cnt_len
#              max_index = x
#      #print len(contours)
#     cv2.drawContours(newFrame,contours[max_index],-1,255,-1)
#     mu = cv2.moments(contours[max_index],False)
    #centerOfMass = (int( mu['m10']/mu['m00']),int( mu['m01']/mu['m00']))
    #mu.get_m10()
    #cv2.circle(newFrame, centerOfMass, 2, (140,140,140), 1 );
    #print win32con
    #print centerOfMass
    #win32api.SetCursorPos(centerOfMass)
    #cv2.imshow("preview", framegray)
    cv2.imshow("output",justSkin)
    #print len(contours)
    #cv2.findContours()
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    #if key ==32:
        #cv2.imwrite(utility.rand_string()+".jpg",justSkin )
    

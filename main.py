import cv2
import numpy as np
from hand import writeText
import constants
import face as Face
import face2
import hand as Hand
 
c = cv2.VideoCapture(0)



MAX_HSV = (166,91,139)
MIN_HSV = (120,30,47)

H = 166
S = 91
V = 139

lowH = 120
lowS = 30
lowV = 47


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


def show(str):
    global messages
    messages.append(str)


def writeText(im, str):
    i = 50
    for message in messages:
        cv2.putText(im, str, (i,i), cv2.FONT_HERSHEY_SIMPLEX, 1.0, WHITE)
        i = i + 50        
        
### Background Removal

def background_removal(f):
    
    cv2.accumulateWeighted(f, avg1, 0.5)     
    res1 = cv2.convertScaleAbs(avg1)
    res2 = cv2.convertScaleAbs(avg2)
    of = f.copy()    
    res3 = res2.copy()
    of = cv2.subtract(of, res3)
    f = cv2.subtract(res2, f) 
    of = cv2.inRange(of, (0,0,0), (20,20,20))
    cv2.bitwise_not(of, of)
    of = cv2.erode(of,cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3)))
    of = cv2.erode(of,cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3)))
    of = cv2.dilate(of,cv2.getStructuringElement(cv2.MORPH_RECT,(6, 6)))
    of = cv2.dilate(of,cv2.getStructuringElement(cv2.MORPH_RECT,(6, 6)))
    f = cv2.inRange(f ,constants.Min, constants.Max)
    f = cv2.add(of, f)
    return f 

### Face Detection

def createFaceDetectors():
    d1 = Face.FaceDetector(constants.DETECTOR_TYPE_LPB_FRONT)
    d2= Face.FaceDetector(constants.DETECTOR_TYPE_HAAR_FRONT)
    d3= Face.FaceDetector(constants.DETECTOR_TYPE_LPB_FRONT)
    return d1, d2, d3

def detectFaces(im, d1, d2, d3):
    f1 = d1.detect_faces(im)
    f2 = d2.detect_faces(im)
    f3 = d3.detect_faces(im)
    return f1, f2, f3

def removeFaces(im, faces1, faces2, faces3):
    if len(faces1) > 0:
        bb1  = faces1[0]
        (x,y,w,h) = faces1[0]
        cv2.rectangle(im, (x,y), (x+w,y+h), 0, constants.CV_FILLED)
             
    if len(faces2) > 0:
        bb2  = faces2[0]
        (x,y,w,h) = faces2[0]
        cv2.rectangle(im, (x,y), (x+w,y+h), 0, constants.CV_FILLED)
       
    if len(faces3) > 0:
        bb3  = faces3[0]
        (x,y,w,h) = faces3[0]
        cv2.rectangle(im, (x,y), (x+w,y+h), 0, constants.CV_FILLED)


if c.isOpened():
    _,f = c.read()
else:
    _ = False
    
f = cv2.flip(f, 1)
 
avg1 = np.float32(f)
avg2 = np.float32(f)

i = 0

messages = []
faces = []

iterations = 0 
cam_height = f.shape[0]
cam_width = f.shape[1]

while _ and iterations < 150:
    _, frame = c.read()
    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (int(cam_width*.43), int(cam_height*.43)), 
                  (int(cam_width*.57),int(cam_height*.57)), 255)
    cv2.imshow("Training",frame)
    iterations += 1
    k = cv2.waitKey(20)
    if k == 27:
        break


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

ft = None
face_detected = False
last_image = None
bb = (0,0,0,0)
while(1):    
    last_image = f
    _ , f = c.read()
    i = i + 1    
    f = cv2.flip(f, 1)

    cv2.createTrackbar("HL", "t2", lowH, 180, trackChangeL("H"))
    cv2.createTrackbar("SL", "t2", lowS, 255, trackChangeL("S"))
    cv2.createTrackbar("VL", "t2", lowV, 255, trackChangeL("V"))
    cv2.createTrackbar("H", "t2", H, 180, trackChange("H"))
    cv2.createTrackbar("S", "t2", S, 255, trackChange("S"))
    cv2.createTrackbar("V", "t2", V, 255, trackChange("V"))
    framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    trainer = cv2.inRange(framegray,(lowH,lowS,lowV),(H,S,V))

    original_f = f.copy()
    f  = background_removal(f)
    
    #Face detectors
    d1, d2, d3 = createFaceDetectors()
    
    # Get a list of faces from each detector
    f1, f2, f3 = detectFaces(original_f, d1, d2, d3)
    faces = f1,f2,f3
    if len(f1) > 0:
        new_ft = face2.FaceTracker(original_f, f1[0])
        x,y,w,h = f1[0]
        if not face_detected:
            face_detected = True
            ft = new_ft
            cv2.rectangle(f, (x,y), (x+w, y+h), 255)
        else:
            bb = ft.track(original_f)
            #check to make sure this doesn't suck?
            if not new_ft.compare_trackers(ft):
                ft = new_ft
            elif bb is not None:
                x,y,w,h = bb
            cv2.rectangle(f, (x,y), (x+w, y+h), 255)
            #make sure that this face is not a different face
            #if so, track this one instead
    elif face_detected:
        bb = ft.track(original_f)
        #check to make sure this doesn't suck?
        #if not ft.check_tracker(image):
        #    face_detected = False
        #else:
        if bb is not None:
            x,y,w,h = bb
            cv2.rectangle(f, (x,y), (x+w, y+h), 255)

    #removes faces, modifies image
    removeFaces(f, f1,f2,f3)
    
    justSkinFrame = Hand.filter_skin(original_f)
    
    clean = cv2.bitwise_and(justSkinFrame, f)
    
    clean = Hand.clarify_image(clean)
    
    #Maybe run canny edge detector
    
    c2 = clean.copy()
    contours = Hand.getLargestCountour(c2)
    #cv2.drawContours(clean, contours ,-1,(255,255,255),-1)
    #contours = Hand.getLargestCountour(clean)
    hand_model = Hand.processContours(contours,c2)
     
    if hand_model is not None:
        for hand in hand_model:
            (palm, handCircle, defects, contour, fingers) = hand
            Hand.defineHand(clean, palm, handCircle, defects, contour, fingers, (cam_width, cam_height))
    

    
    writeText(f, str(i))
    #cv2.imshow('hand_model',hand_model)
    cv2.imshow('Clean',clean)
    cv2.imshow('Back',f)
    cv2.imshow('Skin',justSkinFrame)
    cv2.imshow('t2',trainer)
    k = cv2.waitKey(20)
    if k == 27:
        break
 
cv2.destroyAllWindows()
c.release()

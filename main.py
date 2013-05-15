import cv2
import numpy as np
from hand import writeText
import constants
import face as Face
import hand as Hand
 
c = cv2.VideoCapture(0)
cam_height = camera.get(CV_CAP_PROP_FRAME_HEIGHT)
cam_width = camera.get(CV_CAP_PROP_FRAME_WIDTH)

_,f = c.read()
f = cv2.flip(f, 1)
 
avg1 = np.float32(f)
avg2 = np.float32(f)

i = 0

messages = []
faces = []

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

ft = None
face_detected = False

bb = (0,0,0,0)
last_image = f
while(1):
    
    _ , f = c.read()
    i = i + 1    
    f = cv2.flip(f, 1)
    original_f = f.copy()
    f  = background_removal(f)
    
    #Face detectors
    d1, d2, d3 = createFaceDetectors()
    
    # Get a list of faces from each detector
    f1, f2, f3 = detectFaces(original_f, d1, d2, d3)
    faces = f1,f2,f3
    if len(faces) > 0:
        new_ft = face2.FaceTracker(f, faces[0])
        x,y,w,h = faces[0]
        if not face_detected:
            face_detected = True
            ft = new_ft
            cv2.rectangle(f, (x,y), (x+w, y+h), 255)
        else:
            bb = ft.track(f)
            #check to make sure this doesn't suck?
            if not new_ft.compare_trackers(ft):
                ft = new_ft
            elif bb is not None:
                x,y,w,h = bb
            cv2.rectangle(f, (x,y), (x+w, y+h), 255)
            #make sure that this face is not a different face
            #if so, track this one instead
    elif face_detected:
        bb = ft.track(f)
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
    k = cv2.waitKey(20)
    if k == 27:
        break
 
cv2.destroyAllWindows()
c.release()

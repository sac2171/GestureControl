import cv2 as Cv
import numpy as np 
import face as Face


#For use with is skin detector
MAX_HSV = (177,179,139)
MIN_HSV = (138,25,48)
# MAX_HSV = (166,91,139)
# MIN_HSV = (120,30,47)

EMPTY_BOUNDING_BOX = (0,0,0,0)

BGR_RED = (0,0,255)
BGR_BLUE = (255,0,0)
BGR_GREEN = (0,255,0)

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
    #im = Cv.cvtColor(im,Cv.COLOR_RGB2HSV)
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
        if area < 4e3: smallContours.append(index)
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
    

def distance(cent1, cent2):    
    x = abs(cent1[0] - cent2[0])
    y = abs(cent1[1] - cent2[1])
    d = np.sqrt(x**2+y**2)
    return d

    

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
        
        bb1 = EMPTY_BOUNDING_BOX
        bb2 = EMPTY_BOUNDING_BOX
        bb3 = EMPTY_BOUNDING_BOX        
        
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
            Cv.rectangle(im, (x,y), (x+w,y+h), 0, CV_FILLED)
                    
        im = Cv.blur(im, (9,9))    
        im = filter_skin(im)
        skin_im = im.copy();
        
        countours = getLargestCountour(skin_im)
        
        old_im = im.copy()
        
        if countours is not None:
            for countour in countours:
                area = Cv.contourArea(countour)
                
                # create blank image
                
                old_im = Cv.subtract(old_im, im)
                
                last = None
                hull = Cv.convexHull(countour)
                for hu in hull:
                    if last == None:
                        Cv.circle(old_im, tuple(hu[0]), 10, BGR_RED, 5)
                    else:
                        dist = distance(last, tuple(hu[0]))
                        if dist > 40:
                            Cv.circle(old_im, tuple(hu[0]), 10, BGR_RED, 5)
                    last = tuple(hu[0])
        
                #hull=cv2.convexHull()
                hull = Cv.convexHull(countour,returnPoints = False)
                defects = Cv.convexityDefects(countour,hull)
                if defects is not None:         
                    for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        if d > 1000 :
                            start = tuple(countour[s][0])
                            end = tuple(countour[e][0])
                            far = tuple(countour[f][0])                    
                            Cv.circle(old_im,far,5,[0,255,255],-1)                    
                            Cv.line(old_im, start, far, [255, 0, 0], 5) 
                            Cv.line(old_im, far, end, [255, 0, 0], 5)                    
                            #angles.append(self.angle(far, start, end))
        
        #Cv.
        Cv.putText(im, 'Hello World', (100,100), Cv.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0))
        
        #contours, hierarchy = cv2.findContours(filter_,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        
        
        final = Cv.add(im, old_im) 
        
        Cv.imshow('Hand', final)
#         Cv.imshow('Hand', im)
        
        rc, orig_frame = camera.read()
        
        key = Cv.waitKey(20)    
        if key == ESCAPE_KEY_CODE:
            break
    
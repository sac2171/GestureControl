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

BLACK = (0,0,0)
WHITE = (255,255,255)

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
ERODE = 3
DILATE = 10

def filter_skin(im):
    #im = Cv.cvtColor(im,Cv.COLOR_RGB2HSV)
    im = Cv.cvtColor(im,Cv.COLOR_BGR2HSV)
    #im = Cv.cvtColor(im,Cv.COLOR_BGR2RGB)
    
    filter_im = Cv.inRange(im ,MIN_HSV, MAX_HSV )
    #filter_im = Cv.inRange(im,MIN_RGB, MAX_RGB)
    return filter_im

def clarify_image(im):
    im = Cv.erode(im,Cv.getStructuringElement(Cv.MORPH_ELLIPSE,(ERODE, ERODE)))
    #im = Cv.erode(im,Cv.getStructuringElement(Cv.MORPH_ELLIPSE,(ERODE, ERODE)))
    #im = Cv.dilate(im,Cv.getStructuringElement(Cv.MORPH_RECT,(DILATE, DILATE)))
    #im = Cv.dilate(im,Cv.getStructuringElement(Cv.MORPH_RECT,(DILATE, DILATE)))
    #im = Cv.dilate(im,Cv.getStructuringElement(Cv.MORPH_RECT,(DILATE, DILATE)))
    #im = Cv.blur(im, (9,9))  
    #im = Cv.dilate(im,Cv.getStructuringElement(Cv.MORPH_ELLIPSE,(DILATE, DILATE)))
    return im

def getLargestCountour(im):
    #Get all contours
    contours, hierarchy = Cv.findContours(im,Cv.RETR_EXTERNAL, Cv.CHAIN_APPROX_SIMPLE)    
    
    
    smallContours = []
    for index in range(len(contours)):
        area = Cv.contourArea(contours[index])
        if area < 4e3: smallContours.append(index)
        smallContours.sort(reverse=True)        
    for index in smallContours: 
        contours.pop(index)
    
    
    if len(contours) != 0:
        lengthOfContours = len(contours[0])
        #length = Cv.arcLength(contours,False)
        #contours = Cv.approxPolyDP(contours,0.1*length,True)
        simpContours = [Cv.approxPolyDP(cnt,5, True) for cnt in contours]
#         for cnt in contours:            
#             cnt = contours[0] #should only find one contour
#             curve = .01*Cv.arcLength(cnt,True)
#             cnt = Cv.approxPolyDP(cnt,curve,True)
        
        Cv.drawContours(im, simpContours,-1,(64,255,85),-1)
        return simpContours
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

def writeText(im, str):
    Cv.putText(im, str, (50,50), Cv.FONT_HERSHEY_SIMPLEX, 1.0, WHITE)

def writeText2(im, str):
    Cv.putText(im, str, (50,80), Cv.FONT_HERSHEY_SIMPLEX, 1.0, WHITE)
    
def writeText3(im, str):
    Cv.putText(im, str, (50,80), Cv.FONT_HERSHEY_SIMPLEX, 1.0, WHITE)

old_radius = 0

def defineHand(im, palm, handCircle,defects, contour, fingers):
    (x1,y1),radius1 = palm
    (x2,y2),radius2 = handCircle
    
    
    #writeText2(im, str(radius1) + ' ' + str(radius2))
    filtered = filter(lambda a:a<90, fingers)
    numFingers = len(filtered)
    writeText2(im, str(len(defects)) + ' ' + str(len(contour)) + ' ' +  str(numFingers))
    print str(radius1) + ' ' + str(radius2)
    global old_radius
    radius1 = (radius1 + old_radius)/2
    if radius1*1.5 < radius2:
        writeText(im, 'OpenHand')
    else:
        writeText(im, 'Fist')
    old_radius = radius1
#     if(hand.isFist):
#         writeText('Fist')
#     elif(hand.isPoint):
#         writeText('Point')
#     elif(hand.isShoot):
#         writeText('Shooter')
#     elif(hand.isOpen):
#         writeText('Open')
    
    return ''
    
    
def drawHull(contours, old_im):
    last = None
    hull = Cv.convexHull(countour)
    for hu in hull:
        if last == None:
            Cv.circle(old_im, tuple(hu[0]), 10, WHITE, 5)
        else:
            dist = distance(last, tuple(hu[0]))
            if dist > 40:
                Cv.circle(old_im, tuple(hu[0]), 10, WHITE, 5)
        last = tuple(hu[0])
    return hull
        
def getDefects(countour, old_im):
    fingers = []
    hull = Cv.convexHull(countour,returnPoints = False)
    defects = Cv.convexityDefects(countour,hull)
    if defects is not None:         
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            if d > 1000 :
                start = tuple(countour[s][0])
                end = tuple(countour[e][0])
                far = tuple(countour[f][0])                    
                Cv.circle(old_im,far,5,[255,255,255],-1)                    
                Cv.line(old_im, start, far, [255, 0, 0], 5) 
                Cv.line(old_im, far, end, [255, 0, 0], 5)
                fingers.append(angle(far,start,end))
    return defects, fingers

def drawPalm(contour, defects, im):
    farPoints=[]
    #np.ndarray     
    if defects is not None:         
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            if d > 2000 :
                listTwo =[]
                point = tuple(countour[f][0])
                listTwo.append(point)
                far =np.array(listTwo)
                farPoints.append(far)
    array= np.array(farPoints)
    
    if(len(array)>0):
        (x,y),radius = Cv.minEnclosingCircle(array)
        center = (int(x),int(y))
        radius = int(radius)
        Cv.circle(old_im,center,radius,WHITE,-1)
        return (x,y),radius 
    else:
        return (0,0), -1
    
def angle( cent, rect1, rect2):
    v1 = (rect1[0] - cent[0], rect1[1] - cent[1])
    v2 = (rect2[0] - cent[0], rect2[1] - cent[1])
    dist = lambda a:np.sqrt(a[0] ** 2 + a[1] ** 2)
    angle = np.arccos((sum(map(lambda a, b:a*b, v1, v2))) / (dist(v1) * dist(v2)))
    angle = abs(np.rad2deg(angle))
    return angle
    
def convertPoints(points):
    return points

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
        #last_frame = orig_frame
    else:
        rc = False
    
    mog = Cv.BackgroundSubtractor()
    i = 0
    while rc:
        
        #Flip so that hand will move in correct direction
        im = Cv.flip(orig_frame, 1)
        i = i + 1
        #mog 

        
        final = mog.apply(im)
        #im = Cv.blur(blur_constant)
        
#         faces1 = d1.detect_faces(im)
#         faces2 = d2.detect_faces(im)
#         faces3 = d3.detect_faces(im)
#         
#         bb1 = EMPTY_BOUNDING_BOX
#         bb2 = EMPTY_BOUNDING_BOX
#         bb3 = EMPTY_BOUNDING_BOX        
#         
#         if len(faces1) > 0:
#             bb1  = faces1[0]
#             (x,y,w,h) = faces1[0]
#             Cv.rectangle(im, (x,y), (x+w,y+h), 255, CV_FILLED)
#             
#         if len(faces2) > 0:
#             bb2  = faces2[0]
#             (x,y,w,h) = faces2[0]
#             Cv.rectangle(im, (x,y), (x+w,y+h), 180, CV_FILLED)
#             #region_of_interest = im[x:x+w, y,y+h]
#             #hsv = Cv.cvtColor(region_of_interest, Cv.COLOR_BGR2HSV)
#             #Cv.putText(hsv.__str__())  
#          
#         if len(faces3) > 0:
#             bb3  = faces3[0]
#             (x,y,w,h) = faces3[0]
#             Cv.rectangle(im, (x,y), (x+w,y+h), 0, CV_FILLED)
        
         
        
        #im = Cv.blur(im, (3,3))
        im = filter_skin(im)
        #im = Cv.blur(im, (3,3))
        #im = Cv.erode(im,Cv.getStructuringElement(Cv.MORPH_RECT,(ERODE, ERODE)))
        #im = Cv.erode(im,Cv.getStructuringElement(Cv.MORPH_RECT,(ERODE, ERODE)))
        #im = Cv.dilate(im,Cv.getStructuringElement(Cv.MORPH_RECT,(DILATE, DILATE)))
        #Cv.drawContours(final, countours,-1,(64,255,85),-1)
        #im = clarify_image(im)
        
        #skin_im = im.copy();
        
        countours = 0
        #countours = getLargestCountour(im)
        
        old_im = im.copy()
        
        if 0:
            if countours is not None:
                for countour in countours:
                       
                    # create blank image
                    old_im = Cv.subtract(old_im, im)
                    drawHull(countour, old_im)
                     
                    defects, fingers = getDefects(countour, old_im)
                    (x,y),radius = drawPalm(countour, defects, old_im)
                    palm = (x,y),radius                     
     
                     
                    M = Cv.moments(countour)
                    centroid_x = int(M['m10']/M['m00'])
                    centroid_y = int(M['m01']/M['m00'])
                    Cv.circle(old_im, (centroid_x, centroid_y), 20, WHITE, 10)
                     
                    ellipse = Cv.fitEllipse(countour)
                    Cv.ellipse(im,ellipse,WHITE,2)                 
                     
                     
                    (x,y),radius = Cv.minEnclosingCircle(countour)
                    handCircle = (x,y),radius 
                    center = (int(x),int(y))
                    radius = int(radius)
                    Cv.circle(old_im,center,radius,WHITE,2)
                    #writeText(old_im, str(radius))
                     
                    defineHand(old_im, palm, handCircle, defects, countour, fingers)        
        
        #final = old_im
        #final = Cv.add(im, old_im)
        #Cv.drawContours(final, countours,-1,(64,255,85),-1)
        
        Cv.imshow('Other', old_im)
        Cv.imshow('Masked', final)
        #last_frame = final
#         Cv.imshow('Hand', im)
        
        rc, orig_frame = camera.read()
        
        key = Cv.waitKey(20)    
        if key == ESCAPE_KEY_CODE:
            break
    
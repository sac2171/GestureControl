import cv2
import numpy as np 
import face as Face
import OSWrapper as Wrap


#For use with is skin detector
MAX_HSV = (192,179,139)
MIN_HSV = (138,25,40)
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



cv2_FILLED = -1

camera_number = 0
DETECTOR_TYPE_HAAR_DEF_FRONT = 1;
DETECTOR_TYPE_HAAR_FRONT = 2;
DETECTOR_TYPE_LPB_FRONT = 0;

ESCAPE_KEY_CODE = 27
blur_constant = 4

SMOOTH_VARIABLES = (8,8)
ERODE = 3
DILATE = 8

#wrap = OSWrapper()

def filter_skin(im):
    #im = cv2.cv2tColor(im,cv2.COLOR_RGB2HSV)
    im = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    #im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    
    filter_im = cv2.inRange(im ,MIN_HSV, MAX_HSV )
    #filter_im = cv2.inRange(im,MIN_RGB, MAX_RGB)
    return filter_im

def clarify_image(im):
    im = cv2.erode(im,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ERODE, ERODE)))
    #im = cv2.erode(im,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ERODE, ERODE)))
    
    im = cv2.dilate(im,cv2.getStructuringElement(cv2.MORPH_RECT,(DILATE, DILATE)))
    im = cv2.dilate(im,cv2.getStructuringElement(cv2.MORPH_RECT,(DILATE, DILATE)))
    #im = cv2.dilate(im,cv2.getStructuringElement(cv2.MORPH_RECT,(DILATE, DILATE)))

    #im = cv2.blur(im, (3,3))  
    return im

def getLargestCountour(im):
    #Get all contours
    contours, hierarchy = cv2.findContours(im,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)    
    
    
    smallContours = []
    for index in range(len(contours)):
        area = cv2.contourArea(contours[index])
        if area < 4e3: smallContours.append(index)
        smallContours.sort(reverse=True)        
    for index in smallContours: 
        contours.pop(index)
    
    
    if len(contours) != 0:
        lengthOfContours = len(contours[0])
        simpContours = [cv2.approxPolyDP(cnt,2, True) for cnt in contours]        
        #cv2.drawContours(im, simpContours,-1,(64,255,85),-1)
        return simpContours
    else: 
        0 


def remove_face(im, bb):
    print ''
    #im.cv2
    
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
    cv2.putText(im, str, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, WHITE)

def writeText2(im, str):
    cv2.putText(im, str, (50,80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, WHITE)
    
def writeText3(im, str):
    cv2.putText(im, str, (50,80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, WHITE)

old_radius = 0

def defineHand(im, palm, handCircle,defects, contour, fingers, cam_res):
    (x1,y1),radius1 = palm
    (x2,y2),radius2 = handCircle
    
    
    #writeText2(im, st    r(radius1) + ' ' + str(radius2))
    
    x,y,w,h = cv2.boundingRect(contour)
    cv2.rectangle(im,(x,y),(x+w,y+h),WHITE,1)
    
    ratio = w/float(h)
    bb = im[y:y+h-1, x:x+w-1]
    whiteCount = cv2.countNonZero(bb)
    Area = w * h
    percentage = whiteCount/float(Area)
    
    
    filtered = filter(lambda a:a<90, fingers)
    numFingers = len(filtered)
    d = 0
    if defects is not None:         
        for i in range(defects.shape[0]) :
            s,e,f,d = defects[i,0]
            if d > 2000 :
                d = d + 1
    
    #writeText2(im, str(ratio) + ' ' +str(percentage)  + ' ' +  str(numFingers))
    writeText2(im,  str(numFingers))
    
    global old_radius
    radius1 = (radius1 + old_radius)/2
    print str(radius1) + ' ' + str(radius2)

    comp_res = Wrap.getResolution()
    x_tmp = (x2 - float(cam_res[0])/2)*float(comp_res[0])/cam_res[0]
    y_tmp = (y2 - float(cam_res[1])/2)*float(comp_res[1])/cam_res[1]
    x2 = float(comp_res[0])/2 + 2*x_tmp
    y2 = float(comp_res[1])/2 + 2*y_tmp
    x2 = int(x2)
    y2 = int(y2) 
    
    if( numFingers >=4 or (numFingers == 3 and percentage >.75)):
        writeText(im, 'OpenHand')
        Wrap.scrollMouse(x2,y2)
    elif(  ratio >.33 and ratio<.6 ):
        writeText(im, 'Point')
        Wrap.moveMouse(x2,y2)
    elif( percentage >.6 and percentage <.9):
        writeText(im, 'Fist')
    elif( percentage >.33 and percentage <.6 ):
        writeText(im, 'Click')
        Wrap.click(x2,y2)
    else:
        writeText(im, 'Unknown')
    
    old_radius = radius1

    
    return ''
    
    
def drawHull(contours, old_im):
    last = None
    hull = cv2.convexHull(contours)
    for hu in hull:
        if last == None:
            cv2.circle(old_im, tuple(hu[0]), 10, WHITE, 5)
        else:
            dist = distance(last, tuple(hu[0]))
            if dist > 40:
                cv2.circle(old_im, tuple(hu[0]), 10, WHITE, 5)
        last = tuple(hu[0])
    return hull


def getDefects(contour, old_im):
    fingers = []
    hull = cv2.convexHull(contour,returnPoints = False)
    defects = cv2.convexityDefects(contour,hull)
    if defects is not None:         
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            if d > 1500 :
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])
                #cv2.circle(old_im,far,5,[255,255,255],-1)                    
                #cv2.line(old_im, start, far, [255, 0, 0], 5) 
                #cv2.line(old_im, far, end, [255, 0, 0], 5)                    
                fingers.append(angle(far,start,end))
    #array = np.array(farPoints)
    return defects, fingers

def drawPalm(contour, defects, im):
    farPoints=[]
    #np.ndarray     
    if defects is not None:         
        for i in range(defects.shape[0]) :
            s,e,f,d = defects[i,0]
            if d > 2000 :
                listTwo =[]
                far = tuple(contour[f][0])
                #if i == 2:
                    #cv2.circle(im,far,20,[255,255,255],-1)   
                point = tuple(contour[f][0])
                listTwo.append(point)
                far =np.array(listTwo)
                farPoints.append(far)
    array= np.array(farPoints)
    length = len(array)
    if(length>0):
        (x,y),radius = cv2.minEnclosingCircle(array)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(im,center,radius,WHITE,-1)
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

def processContours(contours, im ):
    hand_list = []
    if contours is not None:
        for contour in contours:
               
            # create blank image
            old_im = im.copy() 
            old_im = cv2.subtract(old_im, im)
            drawHull(contour, im)
             
            defects, fingers = getDefects(contour, old_im)
            (x,y),radius = drawPalm(contour, defects, im)
            palm = (x,y),radius                     
        
             
            M = cv2.moments(contour)
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])
            cv2.circle(im, (centroid_x, centroid_y), 20, (0,0,255), 10)
                             
             
             
            (x,y),radius = cv2.minEnclosingCircle(contour)
            handCircle = (x,y),radius 
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(im,center,radius,WHITE,2)
            #writeText(old_im, str(radius))
             
            #defineHand(old_im, palm, handCircle, defects, contour, fingers)
            handObject = palm, handCircle, defects, contour, fingers
            hand_list.append(handObject)
        return hand_list

if __name__ == '__main__':
    
    camera = cv2.VideoCapture(camera_number)
    

    
    
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
        
    cam_height = orig_frame.shape[0]
    cam_width = orig_frame.shape[1]
    
    #mog = cv2.BackgroundSubtractor()
    i = 0
    while rc:
        
        #Flip so that hand will move in correct direction
        im = cv2.flip(orig_frame, 1)
        i = i + 1
        #mog 

        
        final = mog.apply(im)
        #im = cv2.blur(blur_constant)
        
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
#             cv2.rectangle(im, (x,y), (x+w,y+h), 255, cv2_FILLED)
#             
#         if len(faces2) > 0:
#             bb2  = faces2[0]
#             (x,y,w,h) = faces2[0]
#             cv2.rectangle(im, (x,y), (x+w,y+h), 180, cv2_FILLED)
#             #region_of_interest = im[x:x+w, y,y+h]
#             #hsv = cv2.cv2tColor(region_of_interest, cv2.COLOR_BGR2HSV)
#             #cv2.putText(hsv.__str__())  
#          
#         if len(faces3) > 0:
#             bb3  = faces3[0]
#             (x,y,w,h) = faces3[0]
#             cv2.rectangle(im, (x,y), (x+w,y+h), 0, cv2_FILLED)
        
         
        
        #im = cv2.blur(im, (3,3))
        im = filter_skin(im)
        #im = cv2.blur(im, (3,3))
        #im = cv2.erode(im,cv2.getStructuringElement(cv2.MORPH_RECT,(ERODE, ERODE)))
        #im = cv2.erode(im,cv2.getStructuringElement(cv2.MORPH_RECT,(ERODE, ERODE)))
        #im = cv2.dilate(im,cv2.getStructuringElement(cv2.MORPH_RECT,(DILATE, DILATE)))
        #cv2.drawContours(final, countours,-1,(64,255,85),-1)
        #im = clarify_image(im)
        
        #skin_im = im.copy();
        
        countours = 0
        #countours = getLargestCountour(im)
        
        old_im = im.copy()
        
        if 0:
            if countours is not None:
                for contour in countours:
                       
                    # create blank image
                    old_im = cv2.subtract(old_im, im)
                    drawHull(contour, old_im)
                     
                    defects, fingers = getDefects(contour, old_im)
                    (x,y),radius = drawPalm(contour, defects, old_im)
                    palm = (x,y),radius                     
     
                     
                    M = cv2.moments(contour)
                    centroid_x = int(M['m10']/M['m00'])
                    centroid_y = int(M['m01']/M['m00'])
                    cv2.circle(old_im, (centroid_x, centroid_y), 20, WHITE, 10)
                     
                    ellipse = cv2.fitEllipse(contour)
                    cv2.ellipse(im,ellipse,WHITE,2)                 
                     
                     
                    (x,y),radius = cv2.minEnclosingCircle(contour)
                    handCircle = (x,y),radius 
                    center = (int(x),int(y))
                    radius = int(radius)
                    cv2.circle(old_im,center,radius,WHITE,2)
                    #writeText(old_im, str(radius))
                     
                    defineHand(old_im, palm, handCircle, defects, contour, fingers (cam_width,cam_height))        
        
        #final = old_im
        #final = cv2.add(im, old_im)
        #cv2.drawContours(final, countours,-1,(64,255,85),-1)
        
        cv2.imshow('Other', old_im)
        cv2.imshow('Masked', final)
        #last_frame = final
#         cv2.imshow('Hand', im)
        
        rc, orig_frame = camera.read()
        
        key = cv2.waitKey(20)    
        if key == ESCAPE_KEY_CODE:
            break
    
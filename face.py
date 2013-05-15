import cv2
import numpy
import face2

class FaceDetector:

    HAAR_CASCADE_PATH_DEF = "haarcascade_frontalface_default.xml"
    HAAR_CASCADE_PATH_ALT = "haarcascades_haarcascade_frontalface_alt.xml"
    LBP_CASCADE_PATH = "lbpcascade_frontalface.xml"

    def __init__(self, type):
        if type == 1:
            self.cascade_path = self.HAAR_CASCADE_PATH_DEF
        elif type == 2:
            self.cascade_path = self.HAAR_CASCADE_PATH_ALT
        else:
            self.cascade_path = self.LBP_CASCADE_PATH
        self.cascade = cv2.CascadeClassifier(self.cascade_path)
        

    def detect_faces(self, image):
        faces = []
        detected = self.cascade.detectMultiScale(image, 1.2, 2, cv2.CASCADE_DO_CANNY_PRUNING, (100,100))
        if type(detected) is numpy.ndarray:
            for (x,y,w,h)in detected:
                faces.append((x,y,w,h))
        return faces

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    detector = FaceDetector(0)
    ft = None
    faces = []
    num_faces = 0
    face_detected = False

    if capture.isOpened():
        returnValue, image = capture.read()
    else:
        returnValue = False;

    lowH, lowS, lowV = 0,0,0
    H,S,V = 0,0,0
    tracked_faces = list()
    bb = (0,0,0,0)
    last_image = image
    while returnValue:

        gauss = cv2.GaussianBlur(image, (0,0), 3)
        #framegray = cv2.cvtColor(gauss ,cv2.COLOR_BGR2GRAY)
        #hue, saturation, illumination = cv2.split(cv2.cvtColor(gauss, cv2.COLOR_BGR2HSV))
        #illumination = cv2.equalizeHist(illumination)
        #frame = cv2.merge([hue,saturation,illumination])
        #print frame
        faces = detector.detect_faces(image)
        index = 0
        #stop tracking any "bad" faces and update "good" faces
        #for ft in tracked_faces:
        #    if not ft.check_tracker():
        #        tracked_faces.remove(ft)
        #    else:
        #        bb = ft.track(image, last_image, ft.bb)
        #        x,y,w,h = bb
        #        cv2.rectangle(framegray, (x,y), (x+w, y+h), 255)

        #new_faces = list()

        #lowR, lowG, lowB = 0,0,0
        #R,G,B = 0,0,0
        #start tracking any new faces

        if len(faces) > 0:
            new_ft = face2.FaceTracker(image, faces[0])
            x,y,w,h = faces[0]
            if not face_detected:
                face_detected = True
                ft = new_ft
                cv2.rectangle(image, (x,y), (x+w, y+h), 255)
            else:
                bb = ft.track(image)
                #check to make sure this doesn't suck?
                if not new_ft.compare_trackers(ft):
                    ft = new_ft
                elif bb is not None:
                    x,y,w,h = bb
                cv2.rectangle(image, (x,y), (x+w, y+h), 255)
                #make sure that this face is not a different face
                #if so, track this one instead
        elif face_detected:
            bb = ft.track(image)
            #check to make sure this doesn't suck?
            #if not ft.check_tracker(image):
            #    face_detected = False
            #else:
            if bb is not None:
                x,y,w,h = bb
                cv2.rectangle(image, (x,y), (x+w, y+h), 255)

            #    num_faces += 1
            #    if num_faces == 1:
            #        new_ft = face2.FaceTracker(image, face)
            #    else:
            #        bb = new_ft.track(image, last_image, face)
            #        x,y,w,h = bb
            #        cv2.rectangle(framegray, (x,y), (x+w, y+h), 255)
            #    break
        #lowH, lowS, lowV = ft.min_hsv
        #H, S, V = ft.max_hsv
            #lowR, lowG, lowB = new_ft.min_rgb
            #R, G, B = new_ft.max_rgb
            #should_add = True
            #for ft in tracked_faces:
            #    if new_ft.compare_trackers(ft):
            #        should_add = False
            #        break
            #if should_add:
            #    new_faces.append(new_ft)
            #    x,y,w,h = face
            #    cv2.rectangle(framegray, (x,y), (x+w, y+h), 255)
        #tracked_faces.extend(new_faces)

        #print H,S,V, lowH, lowS, lowV
        #justSkin = cv2.inRange(gauss,(lowH,lowS,lowV),(H,S,V))
        #justSkin = cv2.inRange(image,(lowR,lowG,lowB),(R,G,B))
        #cv2.imshow("skin", justSkin)

        #test skin color against old values
        #if different, restart trackers, else keep tracking
        #NOTE: we do not check specifically if len(faces) < num_faces
        #This is because we may be tracking a previous face that has
        #not registered in this frame. We still base whether we drop
        #this face on HSV values

        
        cv2.imshow("test", image)
        last_image = image
        returnValue, image = capture.read()
        key = cv2.waitKey(20)
        if key == 27:
            break

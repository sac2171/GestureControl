import cv2
import numpy
import face2
import threading

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

    if capture.isOpened():
        returnValue, image = capture.read()
    else:
        returnValue = False;

    tracked_faces = list()
    bb, new_bb, last_bb = (0,0,0,0),(0,0,0,0),(0,0,0,0)
    last_image = image
    while returnValue:
        framegray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
        faces = detector.detect_faces(image)

        index = 0
        #stop tracking any "bad" faces and update "good" faces
        for ft in tracked_faces:
            if not ft.check_tracker():
                tracked_faces.remove(ft)
            else:
                bb = ft.camshift_tracking(image, last_image, ft.bb)
                x,y,w,h = bb
                cv2.rectangle(framegray, (x,y), (x+w, y+h), 255)

        new_faces = list()
        #start tracking any new faces
        for face in faces:
            new_ft = face2.FaceTracker(image, face)
            should_add = True
            for ft in tracked_faces:
                if new_ft.compare_trackers(ft):
                    should_add = False
                    break
            if should_add:
                new_faces.append(new_ft)
                x,y,w,h = face
                cv2.rectangle(framegray, (x,y), (x+w, y+h), 255)
        tracked_faces.extend(new_faces)

        #test skin color against old values
        #if different, restart trackers, else keep tracking
        #NOTE: we do not check specifically if len(faces) < num_faces
        #This is because we may be tracking a previous face that has
        #not registered in this frame. We still base whether we drop
        #this face on HSV values

        
        cv2.imshow("test", framegray)
        last_image = image
        returnValue, image = capture.read()
        key = cv2.waitKey(20)
        if key == 27:
            break

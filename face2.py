import cv2
import cv2.cv as cv
import numpy as np

class FaceTracker:
    def __init__(self, image, bb):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        (x,y,w,h) = bb
        boxed_image = hsv[x:x+w,y:y+h]
        maxH = -1
        minH = 181
        for row in boxed_image:
            for pixel in row:
                if pixel[0] > maxH:
                    maxH = pixel[0]
                elif pixel[0] < minH:
                    minH = pixel[0]
        self.min_hsv = (minH, 30, 0)
        self.max_hsv = (maxH, 140, 240)
        self.bb = bb

    def camshift_tracking(self, img1, img2, bb):
        hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(self.min_hsv), np.array(self.max_hsv))
        x0, y0, w, h = bb
        x1 = x0 + w -1
        y1 = y0 + h -1
        hsv_roi = hsv[y0:y1, x0:x1]
        mask_roi = mask[y0:y1, x0:x1]
        hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
        hist_flat = hist.reshape(-1)
        prob = cv2.calcBackProject([hsv,cv2.cvtColor(img2, cv.CV_BGR2HSV)], [0], hist_flat, [0, 180], 1)
        prob &= mask
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        new_ellipse, track_window = cv2.CamShift(prob, bb, term_crit)
        self.bb = track_window
        return track_window

    def compare_trackers(self, other):
        minX = min(self.bb[0], other.bb[0])
        minY = min(self.bb[1], other.bb[1])
        maxX = max(self.bb[0]+self.bb[2], other.bb[0]+other.bb[2])
        maxY = max(self.bb[1]+self.bb[3], other.bb[1]+other.bb[3])
        small_bb_area = min(self.bb[2]*self.bb[3], other.bb[2]*other.bb[3])
        total_area = (maxX - minX)*(maxY-minY)
        if small_bb_area < .7*total_area:
            return False
	return True

    def check_tracker(self):
        pass

def face_track():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        rc, img = cap.read()
    else:
        rc = False
    cv2.namedWindow("CAMShift", cv2.CV_WINDOW_AUTOSIZE)
    #cv2.setMouseCallback("CAMShift",my_mouse_callback )
    
    #(320,158), (320+124,158+124)
    bb =(125,125,200,200) # get bounding box from some method
    while rc:        
        rc, img1 = cap.read()
        #img= cv2.cvtColor(img ,cv2.COLOR_BGR2GRAY)
        #bb = camshift_tracking(img1, img, bb)
        img = img1
        hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

        #draw bounding box on img1
        #x, y, w, h = bb
        #cv2.rectangle(img1, (x,y), (x+w,y+h), 255)
        mask = cv2.inRange(hsv, np.array((0,60,32)), np.array((180,255,255)))

        #cv2.imshow("hsv", hsv)
        cv2.imshow("CAMShift",mask)
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

if __name__ == '__main__': 
    face_track()

import cv2
import cv2.cv as cv
import numpy as np

def camshift_tracking(img1, img2, bb):
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
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
    return track_window

def my_mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'hi'
    if event == cv2.EVENT_LBUTTONUP:
        print 'hi2'
    if event == cv2.EVENT_MOUSEMOVE:
        print 'hi3'

        
def face_track():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        rc, img = cap.read()
    else:
        rc = False
    cv2.namedWindow("CAMShift", cv2.CV_WINDOW_AUTOSIZE)
    cv2.setMouseCallback("CAMShift",my_mouse_callback )
    
    #(320,158), (320+124,158+124)
    bb =(125,125,200,200) # get bounding box from some method
    while rc:        
        rc, img1 = cap.read()
        #img= cv2.cvtColor(img ,cv2.COLOR_BGR2GRAY)
        bb = camshift_tracking(img1, img, bb)
        img = img1
        #draw bounding box on img1
        x, y, w, h = bb
        cv2.rectangle(img1, (x,y), (x+w,y+h), 255)  
        
        cv2.imshow("CAMShift",img1)
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

if __name__ == '__main__': 
    face_track()

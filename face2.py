import cv2
import cv2.cv as cv
import numpy as np

class FaceTracker:

    def __init__(self, image, bb):
        self.hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        self.hue = cv2.split(self.hsv)[0]
        self.mask = self.hue.copy()
        self.prob = self.hue.copy()
        self.hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(self.hsv, (0,55,65),(180,255,255))
        self.hue = cv2.split(self.hsv)[0]
        self.bb = bb
        x,y,w,h = bb
        hue_roi = self.hue[y:y+h-1,x:x+w-1]
        mask_roi = self.mask[y:y+h-1,x:x+w-1]
        self.hist = cv2.calcHist( [hue_roi], [0], mask_roi, [30], [0, 180] )
        cv2.normalize(self.hist, self.hist, 0, 255, cv2.NORM_MINMAX);
        self.hist = self.hist.reshape(-1)


    def track(self, image):
        self.hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(self.hsv, (0,55,65),(180,255,255))
        self.hue = cv2.split(self.hsv)[0]
        self.prob = cv2.calcBackProject([self.hue,self.prob], [0], self.hist, [0, 180], 1)
        self.prob = cv2.bitwise_and(self.prob, self.mask)
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        try:
            new_ellipse, track_window = cv2.CamShift(self.prob, self.bb, term_crit)
        except cv2.error:
            return None
        self.bb = track_window
        return track_window


    # def __init__(self, image, bb):
    #     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #     hsv = image
    #     #rgb_i = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     (x,y,w,h) = bb
    #     boxed_image = hsv[int(y+2*h/5):int(y+4*(h-1)/5),int(x+w/8):int(x+7*(w-1)/8)]
    #     #boxed_image = hsv[int(y+h/2):int(y+h),int(x+w/4):int(x+3*w/4)]
    #     hsv = cv2.split(boxed_image)
    #     #rgb_image = rgb_i[int(y+h/2):int(y+h),int(x+w/4):int(x+3*w/4)]
    #     #rgb = cv2.split(rgb_image)
    #     h = hsv[0]
    #     s = hsv[1]
    #     v = hsv[2]
    #     #r = rgb[0]
    #     #g = rgb[1]
    #     #b = rgb[2]
    #     self.min_hsv = (int(np.median(h)-h.std()), int(np.median(s)-s.std()), int(np.median(v)-v.std()))
    #     self.max_hsv = (int(np.median(h)+h.std()), int(np.median(s)+s.std()), int(np.median(v)+v.std()))
    #     print self.min_hsv, self.max_hsv
    #     #self.min_rgb = (int(r.mean()-r.std()), int(g.mean()-g.std()), int(b.mean()-b.std()))
    #     #self.max_rgb = (int(r.mean()+r.std()), int(g.mean()+g.std()), int(b.mean()+b.std()))
    #     self.bb = bb

    # def camshift_tracking(self, img1, img2, bb):
    #     hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    #     mask = cv2.inRange(hsv, np.array((0,0,0)), np.array((180,255,255)))
    #     x0, y0, w, h = bb
    #     x1 = x0 + w -1
    #     y1 = y0 + h -1
    #     hsv_roi = hsv[y0:y1, x0:x1]
    #     mask_roi = mask[y0:y1, x0:x1]
    #     hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
    #     cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
    #     hist_flat = hist.reshape(-1)
    #     prob = cv2.calcBackProject([hsv,cv2.cvtColor(img2, cv.CV_BGR2HSV)], [0], hist_flat, [0, 180], 1)
    #     prob &= mask
    #     term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
    #     new_ellipse, track_window = cv2.CamShift(prob, bb, term_crit)
    #     self.bb = bb
    #     return track_window

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

    def check_tracker(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        (x,y,w,h) = self.bb
        boxed_image = hsv[int(y+2*h/5):int(y+4*(h-1)/5),int(x+w/8):int(x+7*(w-1)/8)]
        #boxed_image = hsv[int(y+h/2):int(y+h),int(x+w/4):int(x+3*w/4)]
        hsv = cv2.split(boxed_image)
        #rgb_image = rgb_i[int(y+h/2):int(y+h),int(x+w/4):int(x+3*w/4)]
        #rgb = cv2.split(rgb_image)
        h = hsv[0]
        s = hsv[1]
        med_h = h.mean()
        med_s = s.mean()
        if med_h > self.min_hsv[0] and med_h < self.max_hsv[0] and med_s > self.min_hsv[1] and med_s < self.max_hsv[1]:
            return True
        return False

def face_track():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        rc, img = cap.read()
    else:
        rc = False
    cv2.namedWindow("CAMShift", cv2.CV_WINDOW_AUTOSIZE)
    #cv2.setMouseCallback("CAMShift",my_mouse_callback )
    
    ft = FaceTracker
    #(320,158), (320+124,158+124)
    bb =(125,125,200,200) # get bounding box from some method
    while rc:        
        rc, img1 = cap.read()
        #img= cv2.cvtColor(img ,cv2.COLOR_BGR2GRAY)
        bb = camshift_tracking(img1, img, bb)
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
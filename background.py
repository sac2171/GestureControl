import cv2
import numpy as np
 
c = cv2.VideoCapture(0)
_,f = c.read()
 
avg1 = np.float32(f)
avg2 = np.float32(f)

MAX_HSV = (177,179,139)
MIN_HSV = (138,25,48)

Min = (30,30,30)
Max = (255,255,255)
MM = (225, 225,225) 
 
while(1):
    _ , f = c.read()
    

    #im = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    #filter_im = cv2.inRange(im ,MIN_HSV, MAX_HSV )
    
    
    cv2.accumulateWeighted(f, avg1, 0.05)
    #cv2.accumulateWeighted(f, avg2, 0.01)
     
    res1 = cv2.convertScaleAbs(avg1)
    res2 = cv2.convertScaleAbs(avg2)
    
    of = f.copy()
    #ret, res2 = cv2.invert(res2)
    
    other_f = cv2.inRange(res2 ,(0,0,0), Min)
    #other_f = res2
    everything_the_same = cv2.subtract(f, res2)
    f = cv2.subtract(res2, f) 
       
    #f = cv2.add(res1, f)
    #f = cv2.subtract(other_f, f)
    f_after = f.copy()
    everything_the_same = cv2.inRange(everything_the_same, (0,0,0), Min)
    cv2.bitwise_not(everything_the_same, everything_the_same )
    
    #f = cv2.add(everything_the_same, f)
    #everything_the_same = cv2.inRange(everything_the_same, (0,0,0), Min)
    #everything_the_same = cv2.invert(everything_the_same)
    f = cv2.inRange(f ,Min, Max)
    #f = cv2.add(f, other_f)
    
    f_after = cv2.add(f_after, res1)
    #f_after = cv2.addWeighted()
    
    #im = cv2.cvtColor(of,cv2.COLOR_BGR2HSV)
    #filter_im = cv2.inRange(im ,MIN_HSV, MAX_HSV )
    
    f = cv2.add(everything_the_same, f)
    cv2.imshow('im2',everything_the_same)
    cv2.imshow('img',f)    
    #cv2.imshow('avg1',other_f)
    #cv2.imshow('avg2',res2)
    k = cv2.waitKey(20)
 
    if k == 27:
        break
 
cv2.destroyAllWindows()
c.release()
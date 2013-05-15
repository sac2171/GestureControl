import cv2
import numpy as np
 
c = cv2.VideoCapture(0)
_,f = c.read()
 
avg1 = np.float32(f)
avg2 = np.float32(f)

MAX_HSV = (177,179,139)
MIN_HSV = (138,25,48)

Min = (40,40,40)
Max = (255,255,255) 
 
while(1):
    _ , f = c.read()
    

    #im = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    #filter_im = cv2.inRange(im ,MIN_HSV, MAX_HSV )
    
    
    cv2.accumulateWeighted(f, avg1, 0.1)
    #cv2.accumulateWeighted(f, avg2, 0.01)
     
    res1 = cv2.convertScaleAbs(avg1)
    res2 = cv2.convertScaleAbs(avg2)
    
    old_f = f.copy()
    #res2 = cv2.multiply(res2, -1)
    
    #f = cv2.add(f, res2)
    f = cv2.subtract(res2, f)
    f_after = f.copy()
    f = cv2.inRange(f ,Min, Max)
    
    f_after = cv2.add(f_after, res1)
    #f_after = cv2.addWeighted()
    
    im = cv2.cvtColor(old_f,cv2.COLOR_BGR2HSV)
    filter_im = cv2.inRange(im ,MIN_HSV, MAX_HSV )
    
    cv2.imshow('im2',filter_im)
    cv2.imshow('img',f)    
    cv2.imshow('avg1',f_after)
    #cv2.imshow('avg2',res2)
    k = cv2.waitKey(20)
 
    if k == 27:
        break
 
cv2.destroyAllWindows()
c.release()
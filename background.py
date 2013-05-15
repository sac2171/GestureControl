import cv2
import numpy as np
 
c = cv2.VideoCapture(0)
_,f = c.read()
f = cv2.flip(f, 1)
 
avg1 = np.float32(f)
avg2 = np.float32(f)

MAX_HSV = (177,179,139)
MIN_HSV = (138,25,48)

Min = (30,30,30)
Max = (255,255,255)
MM = (225, 225,225) 
i = 0
while(1):
    _ , f = c.read()
    i = i + 1
    f = cv2.flip(f, 1)

    
    
    cv2.accumulateWeighted(f, avg1, 0.5)
    #if(i%1200):
    #   avg2 = np.float32(f)
    #cv2.accumulateWeighted(f, avg2, .1)
     
    res1 = cv2.convertScaleAbs(avg1)
    res2 = cv2.convertScaleAbs(avg2)
    
    of = f.copy()
    
    catchUp = cv2.inRange(res2, (0,0,0), (60,60,60))
    
    res3 = res2.copy()
    #of = cv2.multiply(of,1.03)
    
    of = cv2.subtract(of, res3)
    f = cv2.subtract(res2, f) 
       
    
    
    of = cv2.inRange(of, (0,0,0), (20,20,20))
    cv2.bitwise_not(of, of)
    
    #of = cv2.erode(of,cv2.getStructuringElement(cv2.MORPH_RECT,(6, 6)))
    #of = cv2.dilate(of,cv2.getStructuringElement(cv2.MORPH_RECT,(12, 12)))
    
    f = cv2.inRange(f ,Min, Max)
    
    
    
    
    
    #of = cv2.subtract(of, catchUp)
    f = cv2.add(of, f)
    
    #f = cv2.subtract(f, catchUp)
    cv2.imshow('im2',of)
    cv2.imshow('img',f)    
    cv2.imshow('avg1',catchUp)
    #cv2.imshow('avg2',res2)
    k = cv2.waitKey(20)
 
    if k == 27:
        break
 
cv2.destroyAllWindows()
c.release()
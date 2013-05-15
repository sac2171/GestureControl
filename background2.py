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
 
while(1):
    _ , f = c.read()
    
    f = cv2.flip(f, 1)                   
    
    
    cv2.accumulateWeighted(f, avg1, 0.1)
    #cv2.accumulateWeighted(f, avg2, 0.01)
     
    res1 = cv2.convertScaleAbs(avg1)
    res2 = cv2.convertScaleAbs(avg2)
    
    of = f.copy()
        
    f = cv2.subtract(res2, f)
    of = cv2.subtract(of,res2)

    

    #everything_the_same = cv2.subtract(f, res2)
     


    #everything_the_same = cv2.inRange(everything_the_same, (0,0,0), Min)
    #cv2.bitwise_not(everything_the_same, everything_the_same )

    f = cv2.inRange(f ,Min, Max)
    #of = cv2.inRange(of ,Min, Max)
    

    f# = cv2.add(f,of)

    
    cv2.imshow('of',of)
    cv2.imshow('f',f)    
    #cv2.imshow('avg2',res2)
    k = cv2.waitKey(20)
 
    if k == 27:
        break
 
cv2.destroyAllWindows()
c.release()
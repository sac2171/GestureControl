import cv2
if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    numFrames = 0;
    if camera.isOpened():
        rc, orig_frame = camera.read()
        #last_frame = orig_frame
    else:
        rc = False
    while rc == True:
        numFrames = numFrames + 1
        
        cv2.imshow('background', orig_frame)
        
        
        rc, orig_frame = camera.read()
        
        orig_frame.
        key = cv2.waitKey(20)    
        if key == 27:
            break

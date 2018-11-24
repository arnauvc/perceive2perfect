import numpy as np
import cv2

cap = cv2.VideoCapture(2)

fgbg = cv2.createBackgroundSubtractorMOG2()
i = 0
maxsum = 0

while(1):
    ret, frame = cap.read()
    if ret == 0:
        break
    i=i+1
    fgmask = fgbg.apply(frame)
    currentsum = fgmask.sum()
    if(currentsum > maxsum and i!=1):
        maxsum = currentsum
        print('Nova suma maxima ')
        print(maxsum)
    print('La suma es ')
    print(currentsum)
    if(currentsum>maxsum/5.36):
        print('--------------------- \n esta en moviment \n---------------------')
    cv2.imshow('frame',fgmask)
    previousframe = frame
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
print(maxsum)

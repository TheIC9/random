import cv2 as cv 
import numpy as np 

blank = np.zeros((500,500,3), dtype='uint8')

cv.circle(blank, (200,200) , 50 , (0,0,255), thickness=3)
cv.circle(blank, (200,200) , 49, (0,255,0), thickness=cv.FILLED)
cv.imshow('circle',blank)
cv.waitKey(0)

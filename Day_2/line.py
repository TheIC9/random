import cv2 as cv 
import numpy as np

blank = np.zeros((500,500,3), dtype='uint8')


cv.line(blank, (0,0), (250,250), (0,255,0), thickness=2) # to make the borders
# cv.line(blank, (1,1), (249,249), (0,0,255), thickness=cv.FILLED)# to fill the entire shape
cv.imshow('bruh',blank)

cv.waitKey(0)
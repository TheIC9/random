import cv2 as cv 
import numpy as np

blank = np.zeros((500,500,3), dtype='uint8')
cv.imshow('Blank',blank)
blank[20:30, 300:400] = 255,0,0
cv.imshow('Cat',blank)
cv.waitKey(0)
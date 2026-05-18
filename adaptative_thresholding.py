import cv2 as cv 
import numpy as np 

img = cv.imread('Photos/download.jpg')

gray = cv.cvtColor(img , cv.COLOR_BGR2GRAY)

thresh_adap = cv.adaptiveThreshold(gray,255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,3)

cv.imshow('bw', thresh_adap)

cv.waitKey(0)
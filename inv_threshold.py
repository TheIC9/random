import cv2 as cv 
import numpy as np 

img = cv.imread('Photos/download.jpg')

gray = cv.cvtColor(img , cv.COLOR_BGR2GRAY)

threshold,thresh_inv = cv.threshold(gray, 125, 255, cv.THRESH_BINARY_INV)

cv.imshow('bw', thresh_inv)

cv.waitKey(0)
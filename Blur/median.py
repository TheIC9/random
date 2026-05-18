import cv2 as cv 
import numpy as np 

img = cv.imread('D:\Coding shit\OpenCV\Photos/Dog_1.webp')
# cv.imshow('img',img)
median = cv.medianBlur(img,3)

cv.imshow('median',median)

cv.waitKey(0)
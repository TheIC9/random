import cv2 as cv 
import numpy as np 

img = cv.imread('D:\Coding shit\OpenCV\Photos/Dog_1.webp')
# cv.imshow('img',img)
bilateral = cv.bilateralFilter(img, 10,35,25)

cv.imshow('blur',bilateral)

cv.waitKey(0)
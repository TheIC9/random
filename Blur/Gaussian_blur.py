import cv2 as cv 
import numpy as np 

img = cv.imread('D:\Coding shit\OpenCV\Photos/Dog_1.webp')
# cv.imshow('img',img)
gaussian = cv.GaussianBlur(img,(3,3),0)

cv.imshow('blur',gaussian)

cv.waitKey(0)
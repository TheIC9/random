import cv2 as cv 
import numpy as np 

img = cv.imread('D:\Coding shit\OpenCV\Photos/Dog_1.webp')
# cv.imshow('img',img)
blur = cv.blur(img,(3,3))

cv.imshow('blur',blur)

cv.waitKey(0)
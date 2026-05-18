import cv2 as cv 
import numpy as np

img = cv.imread('Photos/Dog_1.webp')

blank = np.zeros(img.shape[:2] , dtype='uint8')

circle = cv.circle(blank , (img.shape[1]//2,img.shape[0]//2) , 200 , 255 , -1 )

masked = cv.bitwise_and(img,img,mask=circle)

cv.imshow('img',masked)

cv.waitKey(0)

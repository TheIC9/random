import cv2 as cv 
import numpy as np 

img = cv.imread('Photos/Cat_2.webp')

blank = np.zeros(img.shape[:2] , dtype ='uint8')

b,g,r = cv.split(img)
blue = cv.merge([b,blank,blank])
green = cv.merge([ blank,g , blank])
red = cv.merge([blank,blank,r])

new = cv.merge([blue,green,red])
# cv.imshow('b',blue)
# cv.imshow('r',red)
# cv.imshow('g',green)
cv.imshow('merged', new)

cv.waitKey(0)
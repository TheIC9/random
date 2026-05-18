import cv2 as cv
img = cv.imread('Photos/Cat_1.webp')

cv.imshow('Cat', img)

cv.waitKey(0)
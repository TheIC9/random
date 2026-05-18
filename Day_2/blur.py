import cv2 as cv 

img = cv.imread('Photos/Dog_1.webp')

cv.imshow('dog',img)

blur = cv.GaussianBlur(img , (3,3), cv.BORDER_DEFAULT)

cv.imshow('japanese',blur)

cv.waitKey(0)
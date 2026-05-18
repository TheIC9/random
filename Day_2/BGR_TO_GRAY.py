import cv2 as cv 

img = cv.imread('Photos/Cat_1.webp')
cv.imshow('Cat',img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('bw_cat',gray)
cv.waitKey(0)
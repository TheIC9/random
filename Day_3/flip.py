import cv2 as cv 

img = cv.imread('Photos/Dog_2.webp')

flip = cv.flip(img,0)

cv.imshow('Flipped',flip)
cv.waitKey(0)
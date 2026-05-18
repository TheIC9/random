import cv2 as cv 
 
img = cv.imread('Photos/Dog_1.webp')

bruh = cv.Canny(img, 125,175)

cv.imshow('lol',bruh)
cv.waitKey(0)
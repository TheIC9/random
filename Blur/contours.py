import cv2 as cv 
import numpy as np 


img = cv.imread('Photos/Dog_1.webp')

blur = cv.GaussianBlur(img, (5,5), cv.BORDER_DEFAULT)

blank = np.zeros(img.shape, dtype='uint8')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# canny = cv.Canny(blur, 150 ,175)
ret , thresh = cv.threshold(gray, 125 , 255 , cv.THRESH_BINARY)
# cv.imshow('..', thresh)

contours , hierarchies = cv.findContours(thresh, cv.RETR_LIST , cv.CHAIN_APPROX_SIMPLE)

drawn = cv.drawContours(blank, contours, -1 ,(0,255,255),2 )

cv.imshow('drawn', drawn)
print(f"{len(contours)} contour(s) found! ")
# cv.imshow(",,,",thresh)
cv.waitKey(0)

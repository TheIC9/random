import cv2 as cv 
from edge_cascade import bruh
img = cv.imread('Photos/Dog_2.webp')

dialated = cv.dilate(bruh , (3,3), iterations=1)

cv.imshow("idk",dialated)
cv.waitKey(0)
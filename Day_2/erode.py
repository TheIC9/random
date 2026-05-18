import cv2 as cv
from dilated import dialated 

a = cv.erode(dialated, (3,3),iterations=5)

cv.imshow('a',a)
cv.waitKey(0)
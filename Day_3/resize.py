import cv2 as cv 
from rotate import rotated , img 
resized = cv.resize(img , (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow('Resized',resized)
cv.waitKey(0)
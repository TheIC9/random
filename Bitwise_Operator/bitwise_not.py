import cv2 as cv 
import numpy as np 
from bitwise_and import bitwise_and

bitwise_or = cv.bitwise_not(bitwise_and)

cv.imshow('bruh', bitwise_or)

cv.waitKey(0)

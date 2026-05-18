import cv2 as cv 
import numpy as np 
from bitwise import rectangle, circle

bitwise_or = cv.bitwise_or(rectangle,circle)

cv.imshow('bruh', bitwise_or)

cv.waitKey(0)

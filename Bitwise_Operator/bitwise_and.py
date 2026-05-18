import numpy as np 
import cv2 as cv 
from bitwise import rectangle, circle


bitwise_and = cv.bitwise_and(circle,rectangle)
cv.imshow('and',bitwise_and)
cv.waitKey(0)
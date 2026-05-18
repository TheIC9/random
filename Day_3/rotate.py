import cv2 as cv 
import numpy as np 

img = cv.imread('Photos/Cat_2.webp')

def rotate(img, angle, rotPoint= None):
    (height,width) = img.shape[:2]

    if rotPoint is None:
        rotPoint= (width//2,height//2)
    
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width,height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img,45)

cv.imshow('rotatesd',rotated)

cv.waitKey(0)
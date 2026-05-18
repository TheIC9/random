import cv2 as cv 
import numpy as np

blank = np.zeros((500,500,3), dtype='uint8')

cv.putText(blank, 'Hello IC ',(250,250), cv.FONT_HERSHEY_PLAIN, 1.0,(0,0,255),2)
# cv.putText(**canvas**, ' **  text ** ',**(xpos, ypos)**, ** cv.FONT **, **size** ,** color BRG **,** THICKNESS** )
cv.imshow('lol', blank)
cv.waitKey(0)
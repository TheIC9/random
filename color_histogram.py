import cv2 as cv 
import matplotlib.pyplot as plt 
import numpy as np

img = cv.imread('Photos/Dog_2.webp')
blank = np.zeros(img.shape[:2],dtype='uint8')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

circle = cv.circle(blank, (img.shape[1]//2,img.shape[0]//2),100 , 255, -1 )

mask = cv.bitwise_and(gray,gray,mask=circle)
# hist = cv.calcHist([gray], [0] , mask ,[256] ,[0,256])
# # cv.imshow('Gray',hist)
# cv.imshow('Mask', mask)
# plt.plot(hist)
# plt.xlim([0,256])
# plt.show()


colors = ('b','g','r')

for i,col in enumerate(colors):
    hist = cv.calcHist([img],[i],circle,[256],[0,256])
    plt.plot(hist,color=col)
    plt.xlim([0,256])

plt.show()
cv.waitKey(0)
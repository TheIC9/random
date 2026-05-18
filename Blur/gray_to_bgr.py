import cv2 as cv 

img = cv.imread("Photos/images.jpg")

conver = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
conver2 = cv.cvtColor(conver , cv.COLOR_GRAY2BGR)
cv.imshow('img',conver)
print(conver2.shape)
cv.waitKey(0)
import cv2 as cv
img = cv.imread('Photos/Cat_1.webp')

cv.imshow('Cat', img)
def rescaleFrame(frame,scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(frame , dimensions, interpolation=cv.INTER_AREA)
resized = rescaleFrame(img)
cv.imshow('Image', resized)
cv.waitKey(0)
''''''
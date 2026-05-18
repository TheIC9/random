import cv2 as cv
vid = cv.VideoCapture(0) # For using camera not an installed video
# capture = cv.VideoCapture('Videos/cat.')

while True:
    isTrue, frame = vid.read()
    cv.imshow('Camera', vid)

    if cv.waitKey(20) & 0xFF==ord('q'):
        break

vid.release()
cv.destroyAllWindows()
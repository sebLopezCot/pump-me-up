import cv2
import numpy
import sys

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

cap = cv2.VideoCapture(0)

while True:
    #Capture frame by frame
    ret, frame = cap.read()

    flip = cv2.flip(frame, 1) # mirror image

    gray = cv2.cvtColor(flip, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray)

    # Draw a rectangle around the faces
    max_area = 0
    dominant_face = -1
    for i in range(len(faces)):
        area = faces[i][2] * faces[i][3]
        if area > max_area:
            max_area = area
            dominant_face = i

    if dominant_face != -1:
        x, y, w, h = faces[dominant_face]
        cv2.rectangle(flip, (x,y), (x+w, y+h), (0,255,0), 2)

    # Display the resulting frame
    cv2.imshow('Video', flip)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()


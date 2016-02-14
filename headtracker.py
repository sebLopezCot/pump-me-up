import cv2
import numpy
import sys
import time
import math

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

# previous frame variables that change over tiem
lastMag = None
numframes =0
isAwake = False
lastTime = 0
mag = [] #stores 10 previous frames data
t = [] #stores 10 previous frames'

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

        z = w*h #z is area change for depth perception

        cv2.rectangle(flip, (x,y), (x+w, y+h), (0,255,0), 2)
        if lastMag == None:
             lastTime = time.time()
             pass
        elif numframes < 10:
             currentMag = math.sqrt(int(x)**2+ int(y)**2)
             currentTime = time.time()
             changeinT = currentTime - lastTime
             
             lastTime = currentTime #assume that don't move much while running

             mag.append(currentMag)
             t.append(changeinT)
        else:
            currentMag = math.sqrt(int(x)**2+ int(y)**2)

            print currentMag

            currentTime = time.time()
            changeinT = currentTime - lastTime

            lastTime = currentTime #assume that don't move much while running

            mag.append(currentMag)
            t.append(changeinT)
            
            # Calculate average of last 10 frames
            i = 10;
            totalMag = 0;
            totalTime =0;
            avgMag =0;
            while i > 0:
                totalMag += mag[numframes-i]
                i = i-1
            i = 10;
            while i > 0:
                totalTime += t[numframes-i]
                i = i-1
            avgV = totalMag/totalTime

            print avgV

            if abs(avgV) > 100:
                isAwake = True
            print('Is awake = '+ str(isAwake))

        
        # After initial, change lastMag
        lastMag = math.sqrt(x^2+y^2)

        print('x: ' + str(x), 'y: ' + str(y))
        numframes +=1
    # Display the resulting frame
    cv2.imshow('Video', flip)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()


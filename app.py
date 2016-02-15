import cv2
import numpy
import sys
import time
import math
import serial

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

# previous frame variables that change over tiem
lastX = None
lastY= None
numframes =0
isAwake = False
lastTime = 0
xArr = [] #stores 10 previous x values
yArr = [] #stores 10 previous y values
t = [] #stores 10 previous frames'
awake = False
awakeness = 50.0;

motor = "0";
light = "0";

ser = serial.Serial('COM4')
ser.write('0')

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
        if lastX == None:
             lastTime = time.time()
             pass
        elif numframes < 10:
             currentTime = time.time()
             changeinT = currentTime - lastTime
             changeinX = abs(x - lastX)
             changeinY = abs(y - lastY)
             
             lastTime = currentTime #assume that don't move much while running

             xArr.append(changeinX)
             yArr.append(changeinY)
             t.append(changeinT)
        else:
            currentTime = time.time()
            changeinT = currentTime - lastTime
            changeinX = abs(x - lastX)
            changeinY = abs(y - lastY)
             
            lastTime = currentTime #assume that don't move much while running

            xArr.append(changeinX)
            yArr.append(changeinY)
            t.append(changeinT)
            
            # Calculate average of last 10 frames
            i = 10;
            totalX = 0;
            totalY = 0;
            totalTime =0;
            avgX =0;
            avgY =0;
            while i > 0:
                totalX += xArr[numframes-i]
                totalY += yArr[numframes-i]
                totalTime += t[numframes-i]
                i = i-1
            avgX = totalX/totalTime
            avgY = totalY/totalTime
            awake = True if (avgX**2 + avgY**2)**(0.5) > 220.0 else False
            if awake:
                if awakeness < 75.0:
                    awakeness += 1.0
                else:
                    print 'DONE'
            else:
                if awakeness > -100.0:
                    awakeness -= 3.0

            cv2.putText(flip, "avg x: " + str(avgX), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
            cv2.putText(flip, "avg y: " + str(avgY), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
            cv2.putText(flip, "awake: " + str(awake), (20,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
            cv2.putText(flip, "awakeness: " + str(awakeness), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

            if awakeness < 20.0:
                light = "1"
            else:
                light = "0"

            if awakeness < -50.0:
                motor = "1"
            else:
                motor = "0"

            ser.write(light+"\n")

            print avgX
            print avgY

        
        # After initial, change lastMag
        lastX = x
        lastY = y

        print('x: ' + str(x), 'y: ' + str(y))
        numframes +=1
    # Display the resulting frame
    cv2.imshow('Video', flip)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
ser.write("0\n")
ser.close()


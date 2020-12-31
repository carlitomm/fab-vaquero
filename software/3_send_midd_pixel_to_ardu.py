#!/usr/bin/env python2
import cv2
import serial
import time
import string

#global variables
face_central_pixel_x = 0
face_central_pixel_y = 0
errorX = 0

#const values
image_width = 400
image_height = 400
image_center_x = image_width / 2

def detect():
    face_cascade = cv2.CascadeClassifier('./cascades /haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier('./cascades /haarcascade_eye.xml')
    camera = cv2.VideoCapture(0)
    global face_central_pixel_x
    global face_central_pixel_y
    while (True):
        ret, frame = camera.read()
        # frame = cv2.resize(frame, (image_width, image_height))
        # gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(gray, 1.15, 3)
        # for	(x,y,w,h) in faces:
        #     img = cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 2)
        #     face_central_pixel_x = (x + w/2)
        #     face_central_pixel_y = (y + h/2)
        # print ("coordinates: (%r, %r)" %(face_central_pixel_x, face_central_pixel_y))
        # errorX = image_center_x - face_central_pixel_x
        # print errorX
        # cv2.imshow("camera", frame)

        # """
        # SENDING the error to arduino, consider to do this in a separate thread
        # """
        # """
        # arduino.write(str(errorX))
        # if arduino.in_waiting > 0:
        #     data = arduino.readline()
        #     print data
        #     """
        # """
        # end of serial comunication section 
        # """
        if cv2.waitKey(1000/12) & 0xff == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
        #arduino = serial.Serial('/dev/ttyUSB0',115200, timeout=.1)  #serial object to send and receive data eith arduino
        time.sleep(1)                                               #wait for the serial to stablish
        detect()
 
        
        
    
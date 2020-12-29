#!/usr/bin/env python2
import cv2
import serial
import time
import string
import threading

#global variables
face_central_pixel_x = 0
face_central_pixel_y = 0
errorX = 0

#const values
image_width = 400
image_height = 400
image_center_x = image_width / 2

def send_arduino():
    """
    SENDING the error to arduino, consider to do this in a separate thread
    """
    while True:
        
        arduino.write(str(errorX))
        if arduino.in_waiting > 0:
            data = arduino.readline()
            print data
        #print ('hello thread')
        time.sleep(0.01)

def detect():
    #face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    #face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt.xml')
    face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt2.xml')
    #face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt_tree.xml')

    camera = cv2.VideoCapture(1)
    pastTime = 0                                               
    while (True):
        errorX = 0 #default error = 0 
        face_central_pixel_x = image_center_x #default no face detected and error = 0 
        ret, frame = camera.read()
        frame = cv2.resize(frame, (image_width, image_height))
        gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.10, 4, minSize = (70,70), maxSize = (300,300))
        for	(x,y,w,h) in faces:
            img = cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 2)
            face_central_pixel_x = (x + w/2)
            face_central_pixel_y = (y + h/2)

        #print ("coordinates: (%r, %r)" %(face_central_pixel_x, face_central_pixel_y))
        errorX = image_center_x - face_central_pixel_x

        print(time.clock()- pastTime)
        pastTime = time.clock()

        #arduino.write('l')
        #arduino.write(str(errorX))
           
        #print ("error: %r" %(errorX))
        cv2.imshow("camera", frame)
        if cv2.waitKey(1000/12) & 0xff == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #arduino = serial.Serial('/dev/ttyUSB2',115200, timeout=.1)  #serial object to send and receive data eith arduino
    time.sleep(0.1)   
    #sending_thread = threading.Thread(target=send_arduino)
    #sending_thread.start()
    detect()
    
        
        
    
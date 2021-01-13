#!/usr/bin/env python2

import face_recognition
import cv2
import numpy as np
import time
import serial


class face_recognition_module:
    def __init__(self):
        self.face_locations = []
        self.process_this_frame = True
        self.counter = 0
        self.video_capture = cv2.VideoCapture(-1)
        self.face_central_pixel_x = 0
        self.face_central_pixel_y = 0
        self.errorX = 0 
        self.image_center_x = 0
        self.image_center_y = 0
        self.small_frame = 0
        self.rgb_small_frame = 0

    def detect_face_central_pixel(self):
        for (top, right, bottom, left) in (self.face_locations):
            cv2.rectangle(self.small_frame, (left, top), (right, bottom), (0, 0, 255), 2)
            self.face_central_pixel_x = (left + ((right - left)/2))
            self.face_central_pixel_y = (top + ((bottom - top)/2))
    
    def face_coordinates(self):
        return[self.face_central_pixel_x, self.face_central_pixel_y]

    def reshape_image(self, frame):
        self.small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75) 
        image_hight, image_width, color_map = self.small_frame.shape
        self.image_center_x = image_width / 2
        self.image_center_y = image_hight / 2   
        """
        Convert the image from BGR(which OpenCV uses) to RGB (which face_recognition uses)
        """
        self.rgb_small_frame = self.small_frame[:, :, ::-1]
    
    def capture_video_from_webcam(self):
        ret, frame = self.video_capture.read() # Grab a single frame of video
        return frame

    def detect_face(self, frame):        
        self.reshape_image(frame)

        self.errorX = 0 #default error = 0 
        self.face_central_pixel_x = self.image_center_x 
            
        # Only process every other frame of video to save time
        if self.process_this_frame:
            self.face_locations = face_recognition.face_locations(self.rgb_small_frame, number_of_times_to_upsample=1, model="hog")
            self.process_this_frame = False
        self.counter = self.counter + 1
            
        if self.counter == 2:
            self.process_this_frame = True
            self.counter = 0

        self.detect_face_central_pixel()
        self.errorX = self.image_center_x - self.face_central_pixel_x
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.video_capture.release()
            cv2.destroyAllWindows()


    def show_video(self):       
        cv2.imshow("camera", self.small_frame) # Display the resulting image


class face_recognition_haar_cascade(): 
    def __init__(self):
        self.faces = []
        self.face_central_pixel_x = 0
        self.face_central_pixel_y = 0
        self.errorX = 0
        self.image_width = 400
        self.image_height = 400
        self.image_center_x = self.image_width / 2
        #self.face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
        #self.face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt.xml')
        self.face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt2.xml')
        #self.face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt_tree.xml')
        self.video_capture = cv2.VideoCapture(-1)
        time.sleep(1)
     
    def reshape_image(self, frame):
        frame = cv2.resize(frame, (self.image_width, self.image_height))
        gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
        return gray    
    
    def capture_video_from_webcam(self):
        ret, frame = self.video_capture.read() # Grab a single frame of video
        return frame

    def detect_face(self, frame):                                             
        gray = self.reshape_image(frame)

        self.faces = self.face_cascade.detectMultiScale(gray, 1.10, 4, minSize = (70,70), maxSize = (300,300))
        
        self.errorX = 0 #default error = 0 
        self.face_central_pixel_x = self.image_center_x 
                         
        for	(x,y,w,h) in self.faces:
            cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 2)
            self.face_central_pixel_x = (x + w/2)
            self.face_central_pixel_y = (y + h/2)
      
        self.errorX = self.image_center_x - self.face_central_pixel_x
        self.show_video(frame)
        if cv2.waitKey(1000/12) & 0xff == ord("q"):
            self.video_capture.release()
            cv2.destroyAllWindows()
               
    def show_video(self, frame):
        cv2.imshow("camera", frame)   
"""
if __name__ == "__main__":
    #fc = face_recognition_module()
    hc = face_recognition_haar_cascade()

    while True:
        frame = hc.capture_video_from_webcam()  
        hc.detect_face(frame)
        if cv2.waitKey(1000/12) & 0xff == ord("q"):
            cv2.destroyAllWindows()
            break
"""       
        
    
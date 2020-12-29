import face_recognition
import cv2
import numpy as np
import time
import serial

class face_recognition_module:
    def __init__(self):
        self.face_locations = []
        self.fr = face_recognition()
        self.process_this_frame = True
        self.pastTime = 0
        self.counter = 0

        self.video_capture = cv2.VideoCapture(1)

        self.face_central_pixel_x = 0
        self.face_central_pixel_y = 0

        self.errorX = 0 

        self.image_center_x = 0

        self.small_frame = 0
        self.rgb_small_frame = 0

    def detect_face_central_pixel(self):
        for (top, right, bottom, left) in (self.face_locations):
            cv2.rectangle(self.small_frame, (left, top), (right, bottom), (0, 0, 255), 2)
            self.face_central_pixel_x = (left + ((right - left)/2))
    
    def reshape_image(self, frame):
        self.small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75) # Resize frame of video to 3/4 size for faster face recognition processing
        image_hight, image_width, color_map = self.small_frame.shape
        self.image_center_x = image_width / 2   
        """
        Convert the image from BGR(which OpenCV uses) to RGB (which face_recognition uses)
        """
        self.rgb_small_frame = self.small_frame[:, :, ::-1]

    def detect_face(self):
        while True:   
            ret, frame = video_capture.read() # Grab a single frame of video
            self.reshape_image(frame)

            self.errorX = 0 #default error = 0 
            self.face_central_pixel_x = self.image_center_x #default no face detected and error = 0
            
            # Only process every other frame of video to save time
            if self.process_this_frame:
                self.face_locations = self.fr.face_locations(self.rgb_small_frame, number_of_times_to_upsample=1, model="hog")
                self.process_this_frame = False
            self.counter = self.counter + 1
            
            if self.counter == 2:
                self.process_this_frame = True
                self.counter = 0

            self.detect_face_central_pixel()
            self.errorX = self.image_center_x - self.face_central_pixel_x

            self.show_video()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def show_video(self):       
        # Display the resulting image
        cv2.imshow('Video', self.small_frame)


class face_recognition_haar_cascade():
    def __init__(self):
        self.face_central_pixel_x = 0
        self.face_central_pixel_y = 0
        self.errorX = 0

        self.image_width = 400
        self.image_height = 400
        self.image_center_x = image_width / 2
        #self.face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
        #self.face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt.xml')
        self.face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt2.xml')
        #self.face_cascade = cv2.CascadeClassifier('./cascades/frontalFace10/haarcascade_frontalface_alt_tree.xml')

        self.camera = cv2.VideoCapture(1)

        self.faces = []
    def reshape_image(self, frame):
        frame = cv2.resize(frame, (self.image_width, self.image_height))
        gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
        self.faces = self.face_cascade.detectMultiScale(gray, 1.10, 4, minSize = (70,70), maxSize = (300,300))
            
    def detect_face():                                             
        while (True):
            ret, frame = self.camera.read()
            self.reshape_image(frame)

            self.errorX = 0 #default error = 0 
            self.face_central_pixel_x = self.image_center_x #default no face detected and error = 0 
             
            for	(x,y,w,h) in faces:
                img = cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 2)
                self.face_central_pixel_x = (x + w/2)
                self.face_central_pixel_y = (y + h/2)
      
            self.errorX = self.image_center_x - self.face_central_pixel_x

            cv2.imshow("camera", frame)
            if cv2.waitKey(1000/12) & 0xff == ord("q"):
                break
        
        self.camera.release()
        cv2.destroyAllWindows()

#serial object to send and receive data eith arduino
frm = face_recognition_module()
arduino = serial.Serial('/dev/ttyUSB0',115200, timeout=.1)
arduino.write('l')
arduino.write(str(frm.errorX))

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
        
        
    
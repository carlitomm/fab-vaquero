#!/usr/bin/env python2

from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN as MT_slow
from facenet_pytorch import MTCNN
import torch
from matplotlib.patches import Rectangle
from numpy import asarray
from PIL import Image
import cv2
import glob


class FaceDetector(object):
    
    def __init__(self, mtcnn):
        self.mtcnn = mtcnn
    
    def slow_face_detection(self):
        video_capture = cv2.VideoCapture(-1)
        detector = MT_slow(min_face_size=50)
        while True:
            ret, frame = video_capture.read()
            
            faces = detector.detect_faces(frame)
        
            for face in faces:
                x, y, width, height = face['box']
                cv2.rectangle(frame,(x,y), (x+width, y+height), (255,0,0) )

            cv2.imshow("camera", frame) # Display the resulting image
            cv2.waitKey(1) 

        video_capture.release()
        cv2.destroyAllWindows()


    def _draw(self, frame, boxes, probs, landmarks):
        """
        Draw landmarks and boxes for each face detected
        """
        try:
            for box, prob, ld in zip(boxes, probs, landmarks):
                # Draw rectangle on frame
                cv2.rectangle(frame,
                              (box[0], box[1]),
                              (box[2], box[3]),
                              (0, 0, 255),
                              thickness=2)

                # Show probability
                cv2.putText(frame, str(
                    prob), (box[2], box[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Draw landmarks
                cv2.circle(frame, tuple(ld[0]), 5, (0, 0, 255), -1)
                cv2.circle(frame, tuple(ld[1]), 5, (0, 0, 255), -1)
                cv2.circle(frame, tuple(ld[2]), 5, (0, 0, 255), -1)
                cv2.circle(frame, tuple(ld[3]), 5, (0, 0, 255), -1)
                cv2.circle(frame, tuple(ld[4]), 5, (0, 0, 255), -1)
        except:
            pass

        return frame

    def run(self):
        """
            Run the FaceDetector and draw landmarks and boxes around detected faces
        """
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            try:
                # detect face box, probability and landmarks
                boxes, probs, landmarks = self.mtcnn.detect(frame, landmarks=True)
                # draw on frame
                self._draw(frame, boxes, probs, landmarks)

            except:
                pass

            # Show the frame
            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
       
mtcnn = MTCNN()
fcd = FaceDetector(mtcnn)
fcd.slow_face_detection() 
fcd.run()
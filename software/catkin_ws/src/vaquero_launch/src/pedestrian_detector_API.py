from __future__ import print_function
import numpy as np
import argparse
import cv2


class pedestrian_detector ():
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.cap = cv2.VideoCapture(1)
        #self.cv2.startWindowThread()

    def HOG_detect_pedestrian(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (400, 400))
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        boxes, weights = self.hog.detectMultiScale(gray, winStride=(8,8), padding=(8,8), scale=1.02)
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            cv2.waitKey(1)

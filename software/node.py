#!/usr/bin/env python2
import sys
import rospy
import cv2, cv_bridge
from sensor_msgs.msg import Image
import face_recognition_API

class core():
    def __init__(self):
        self.image_sub = rospy.Subscriber("usb_cam/image_raw", Image, self.image_subscriber_cb) 
        self.frame = 0
        self.fc = face_recognition_API.face_recognition_module()

    def image_subscriber_cb(self, msg):
        br = cv_bridge.CvBridge()
        print ("hello")
        self.frame = br.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imshow('camera', self.frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def get_middle_of_face(self):
        self.fc.detect_face(self.frame)
        

if __name__ == "__main__":
    rospy.init_node("vaquero_core")
    #rate = rospy.Rate(10)
    vaquero = core()
    while not rospy.is_shutdown():
        #vaquero.get_middle_of_face()
        rospy.spin()
    
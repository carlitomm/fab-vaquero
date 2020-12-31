#!/usr/bin/env python2
import sys
import rospy
import cv2, cv_bridge
from sensor_msgs.msg import Image
import face_recognition_API
from people_msgs.msg import Person

class core():
    def __init__(self):
        self.fc = face_recognition_API.face_recognition_module()
        self.frame = 0
        self.firstFrameRecieved = False
        
        """
        Ros Variables
        """
        self.person_publisher = rospy.Publisher("person_coordinates", Person)
        self.image_sub = rospy.Subscriber("usb_cam/image_raw", Image, self.image_subscriber_cb) 
    
    def image_subscriber_cb(self, msg):
        br = cv_bridge.CvBridge()
        self.frame = br.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.fc.detect_face(self.frame)
        if self.firstFrameRecieved is False:
            self.firstFrameRecieved = True

    def get_middle_of_face(self):
        if self.firstFrameRecieved is True:
            self.fc.detect_face(self.frame)
            self.fc.show_video()
    
    def cordinates_publisher(self):
        #considering verstical
        person = Person()
        person.position.y, person.position.z = self.fc.face_coordinates()
        self.person_publisher.publish(person) 
        
if __name__ == "__main__":
    rospy.init_node("vaquero_core")
    rate = rospy.Rate(1000)
    vaquero = core()
    while not rospy.is_shutdown():
        vaquero.get_middle_of_face()
        rate.sleep()
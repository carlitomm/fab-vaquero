#!/usr/bin/env python
import rospy
import time
import serial
from sensor_msgs.msg import Range
from people_msgs.msg import Person

class ardu_comm:

    def __init__(self):
        self.connection_success = False
        self.arduino = serial.Serial()
        self.rate = rospy.Rate(1000)
        try:
            self.arduino = serial.Serial('/dev/ttyUSB0',115200, timeout=.1)
            self.connectio_success = True
        except:     
            rospy.logwarn("some error in arduino connection")
        
        """
        things to receive from image node
        """
        self.person_coordinates_x = 0
        self.person_coordinates_y = 0

        self.image_width = 400
        self.image_center_x = self.image_width / 2
        self.errorX = self.image_center_x - self.person_coordinates_x

        """
        Seonsors publisher
        """
        self.tof_pub1 = rospy.Publisher('tof1',Range, queue_size=0)
        self.tof_pub2 = rospy.Publisher('tof1',Range, queue_size=0)
        self.tof_pub3 = rospy.Publisher('tof1',Range, queue_size=0)
        self.tof_pub4 = rospy.Publisher('tof1',Range, queue_size=0)

        """
        subscribers
        """
        self.person_sub = rospy.Subscriber('person_coordinates', Person, self.person_position_cb)

        """
        sensor publisher init
        """
        self.tof1 = Range()
        self.tof2 = Range()
        self.tof3 = Range()
        self.tof4 = Range()
        
        self.tof1.header.frame_id = "/tof1"
        self.tof1.min_range = 50
        self.tof1.max_range = 200

        self.tof2.header.frame_id = "/tof2"
        self.tof2.min_range = 50
        self.tof2.max_range = 200

        self.tof3.header.frame_id = "/tof3"
        self.tof3.min_range = 50
        self.tof3.max_range = 200

        self.tof4.header.frame_id = "/tof4"
        self.tof4.min_range = 50
        self.tof4.max_range = 200

        self.buffer = ""

    def person_position_cb(self, msg):
        if self.arduino.is_open and self.connectio_success is True:
            msg = Person()
            self.person_coordinates_x = msg.position.x
            self.person_coordinates_y = msg.position.y
            self.arduino.write('l')
            self.arduino.write(str(self.errorX))
        else:
            try:
                self.arduino = serial.Serial('/dev/ttyUSB0',115200, timeout=.1)
                self.connectio_success = True
            except:     
                rospy.logwarn("some error in arduino connection")
    
    def sensor_publisher(self):
        while not rospy.is_shutdown():
            if self.arduino.is_open and self.connectio_success is True:
                if self.arduino.in_waiting > 0:
                    i=0
                    data = self.arduino.readline()
                    if data[i] == 't':              #inicia sensores tof
                        buffer = ""
                        i = i+1
                        while data[i] != 'f':
                            buffer += data[i]
                            i = i+1   
                        i = i + 1
                        self.tof1.range = float(buffer)

                        buffer = ""
                        while data[i] != 'f':
                            buffer += data[i]   
                            i = i+1
                        i = i + 1
                        self.tof2.range = float(buffer)

                        buffer = ""
                        while data[i] != 'f':
                            buffer += data[i]   
                            i = i+1
                        i = i + 1
                        self.tof3.range = float(buffer)

                        buffer = ""
                        while data[i] != 'f':
                            buffer += data[i]   
                            i = i+1
                        i = i + 1
                        self.tof4.range = float(buffer)/100
                       
                    self.tof_pub1.publish(self.tof1)
                    self.tof_pub2.publish(self.tof2)
                    self.tof_pub3.publish(self.tof3)
                    self.tof_pub4.publish(self.tof4)
            else:
                try:
                    self.arduino = serial.Serial('/dev/ttyUSB0',115200, timeout=.1)
                    self.connectio_success = True
                except:     
                    rospy.logwarn("some error in arduino connection")
            self.rate.sleep() 
                
if __name__ == "__main__":
    
    rospy.init_node('ardu_comm')
    Ardu_comm = ardu_comm()

    Ardu_comm.sensor_publisher()
        
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
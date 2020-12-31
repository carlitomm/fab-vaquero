#!/usr/bin/env python

import rospy
import time
import actionlib
import serial

from uvbot_core.msg import *
from uvbot_core.srv import *
from std_srvs.srv import SetBool, SetBoolRequest, SetBoolResponse
from sensor_msgs.msg import Range
from std_msgs.msg import String
from std_msgs.msg import Int16
from std_srvs.srv import SetBool

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
        
        self.tof_pub1 = rospy.Publisher('tof1',Range, queue_size=0)
        self.tof_pub2 = rospy.Publisher('tof1',Range, queue_size=0)
        self.tof_pub3 = rospy.Publisher('tof1',Range, queue_size=0)
        self.tof_pub4 = rospy.Publisher('tof1',Range, queue_size=0)
        self.pir_pub = rospy.Publisher('pir', Int16, queue_size=0)

        self.service = rospy.Service('luces_control', SetBool, self.control_luces)
        self.luces_on = False

        self.pir = Int16()
        self.pir.data = 0
        
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

    def control_luces(self, request):
        if self.arduino.is_open and self.connectio_success is True:
            self.luces_on = request.data
            response = SetBoolResponse()
            response.success = True

            if self.luces_on is True:
                response.message = 'ligth are ON'
                self.arduino.write('n')
            if self.luces_on is False:
                response.message = 'ligth are OFF'
                self.arduino.write('l')
        else:
            try:
                self.arduino = serial.Serial('/dev/ttyUSB0',115200, timeout=.1)
                self.connectio_success = True
            except:     
                rospy.logwarn("some error in arduino connection")
        return response
    
    def sensor_publisher(self):
        while not rospy.is_shutdown():
            if self.arduino.is_open and self.connectio_success is True:
                if self.arduino.in_waiting > 0:
                    i=0
                    data = self.arduino.readline()
                    if data[i] == 't':              #inicia seldores tof
                        buffer = ""
                        i = i+1
                        while data[i] != 'f':
                            buffer += data[i]
                            i = i+1   
                        i = i + 1
                        tof1.range = float(buffer)

                        buffer = ""
                        while data[i] != 'f':
                            buffer += data[i]   
                            i = i+1
                        i = i + 1
                        tof2.range = float(buffer)

                        buffer = ""
                        while data[i] != 'f':
                            buffer += data[i]   
                            i = i+1
                        i = i + 1
                        tof3.range = float(buffer)

                        buffer = ""
                        while data[i] != 'f':
                            buffer += data[i]   
                            i = i+1
                        i = i + 1
                        tof4.range = float(buffer)/100
                    
                    self.pir.data = 0
                    if data[i] == 'p':          #p sensor pir
                        buffer = data[i+1]   
                        self.pir.data = int(buffer)
    
                    self.tof_pub1.publish(self.tof1)
                    self.tof_pub2.publish(self.tof2)
                    self.tof_pub3.publish(self.tof3)
                    self.tof_pub4.publish(self.tof4)
                self.pir_pub.publish(self.pir)
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
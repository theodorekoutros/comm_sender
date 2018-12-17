#!/usr/bin/env python

import rospy
import serial
import time
import sys, select, termios, tty
from std_msgs.msg import String
from comm_sender.msg import Comm

class CommSenderNode:
    def __init__(self):
        self.node_name = rospy.get_name()

        rospy.loginfo("[%s] Initialzing." %(self.node_name))     
        
        self.key = None

        self.s = serial.Serial('/dev/ttyACM0')
 
        self.sub_key = rospy.Subscriber("/key", Comm, self.cbKey, queue_size=1)
        self.rate = rospy.Rate(10) # 30hz 

    def cbKey(self, msg):
        self.key = msg.data
               
        if self.key != '':
            rospy.loginfo("Sending.[%s] to serial. " %(self.key))
            self.s.write(self.key)

if __name__=="__main__":
    rospy.init_node('comm_sender_node', anonymous=False)
    node = CommSenderNode()
    rospy.spin()

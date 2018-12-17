#!/usr/bin/env python

import rospy
import serial
import time
import sys, select, termios, tty
from std_msgs.msg import String
from comm_sender.msg import Comm
from gantry_control.msg import *
import act2serial

devname='/dev/ttyACM1'

class CommSenderNode:
    def __init__(self):
        self.node_name = rospy.get_name()

        rospy.loginfo("[%s] Initialzing." %(self.node_name))     
        
        self.sendStr = None

        self.s = serial.Serial(devname)
 
        self.sub_key = rospy.Subscriber("/key", Comm, self.cbKey, queue_size=10)
        self.sub_actuation = rospy.Subscriber("/gantry/set_actuation", actuation, self.cbActuation, queue_size=10)
        self.rate = rospy.Rate(50) # 30hz 

    def sendSer(self)
        if self.sendStr != '':
            rospy.loginfo("Sending.[%s] to serial. " %(self.sendStr))
            self.s.write(self.sendStr+'\n')

    def cbKey(self, msg):
        self.sendStr = msg.data
        self.sendSer()
               

    def cbActuation(self,msg):
        self.sendStr = act2serial.convert(msg.levels)
        self.sendSer()

if __name__=="__main__":
    rospy.init_node('comm_sender_node', anonymous=False)
    node = CommSenderNode()
    rospy.spin()

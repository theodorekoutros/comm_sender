#!/usr/bin/env python

import rospy
import serial
import time
import sys, select, termios, tty
from std_msgs.msg import String
from comm_sender.msg import Comm

class KeyCatcherNode:
    def __init__(self):
        self.node_name = rospy.get_name()

        rospy.loginfo("[%s] Initialzing." %(self.node_name))
        rospy.loginfo("Please hit a/b to activate/deactivate the live output on Arduino IDE. ")
        rospy.loginfo("Please hit l to load the PID parameters. ")
        rospy.loginfo("Please hit 0 to set all the channels to 0 psi. ")
        rospy.loginfo("Please hit y to set the mode to pressure control. ")      
        
        self.settings = termios.tcgetattr(sys.stdin)

        self.pub_key = rospy.Publisher("/key", Comm, queue_size=10)
        
        self.rate = rospy.Rate(10) # 10hz 


    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''        

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key


    def Sender(self):
        #rospy.init_node('talker', anonymous=True)
        message = ''
        while not rospy.is_shutdown():

            key = self.getKey()

            if (key == '\x61'): #small a
                message ='on'
                rospy.loginfo("[%s] Key Input." %(key))
                time.sleep(1)

            elif (key == '\x62'): #small b
                message ='off'
                rospy.loginfo("[%s] Key Input." %(key))
                time.sleep(1)

            elif (key == '\x74'): #small t 
                message ='TIME;100'
                rospy.loginfo("[%s] Key Input." %(key))
                time.sleep(1)

            elif (key == '\x6C'): #small l 
                message ='LOAD;'
                rospy.loginfo("[%s] Key Input." %(key))
                time.sleep(1)

            elif (key == '\x79'): #small y 
                message ='MODE;1'
                rospy.loginfo("[%s] Key Input." %(key))
                time.sleep(1)

            elif (key == '\x30'): #0 
                message ='SET;0'
                rospy.loginfo("[%s] Key Input." %(key))
                time.sleep(1)

            elif (key == '\x31'): #1 
                message ='SET;0;5;5;5;0;0'
                rospy.loginfo("[%s] Key Input." %(key))
                time.sleep(1)

            elif (key == '\x32'): #2 
                message ='SET;0;10;10;10;0;0'
                rospy.loginfo("[%s] Key Input." %(key))
                time.sleep(1)
            
            elif (key == '\x03'):
                message ='off'
                self.pub_key.publish(message)
                rospy.loginfo("[%s] Turning off feed. Wait 1 second.")
                time.sleep(1)
                rospy.loginfo("[%s] Hit Control-C to exit.")
                break
            #else:
                #rospy.loginfo("[%s] Key Input." %(key))
                #continue with the pressure adaptation input

            self.pub_key.publish(message)
            message = ''

            self.rate.sleep()

if __name__=="__main__":
    rospy.init_node('key_catcher_node', anonymous=False)
    node = KeyCatcherNode()
    node.Sender()
    rospy.spin()

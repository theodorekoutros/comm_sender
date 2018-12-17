#!/usr/bin/env python

import rospy
from std_msgs.msg import String

class ListenerNode:
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initialzing." %(self.node_name))

        self.sub_key = rospy.Subscriber("/key", String, self.callback, queue_size=1)

    def callback(self,msg):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', msg.data)

if __name__=="__main__":
    rospy.init_node('listener_node', anonymous=False)
    node = ListenerNode()
    rospy.spin()

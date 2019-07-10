#!/usr/bin/env python


#Adapted from:
#https://answers.ros.org/question/159276/read-data-from-serial-port-and-publish-over-a-topic/


import roslib;  # roslib.load_manifest('numpy_tutorials') #not sure why I need this
import rosbag
import rospy
import serial
from comm_sender.msg import serial_data
from std_msgs.msg import String
#import serial_coms

class SerialTalkerNode:
	def __init__(self):
		self.node_name = rospy.get_name()
		rospy.loginfo("[%s] Initialzing." %(self.node_name))  

		#Getting parameters from launch file
		self.devname = rospy.get_param("/devname")
		self.baud = rospy.get_param("/baudrate")		

		#Initilizing serial communication
		self.resume()
		self.initialize()

		#Publishers and Subscribers
		self.pub = rospy.Publisher('/pressure_control/location', serial_data, queue_size=10)
		self.pubRaw = rospy.Publisher('/pressure_control/raw', String, queue_size=10)

		self.rate = rospy.Rate(10)
	
	def resume(self):
		"""Start serial communication
		INPUTS:
			devname - the short name of the device you want to use
			baud    - baud rate
		OUTPUTS:
			s - the serial object created
		"""	
		self.ser = serial.Serial(self.devname, self.baud)
		if not self.ser.isOpen():
			self.ser.open()
			

	def initialize(self):
		self.ser.flushInput()	

	def talker(self):

		while not rospy.is_shutdown():
			if self.ser.in_waiting: 
				try:
					data= self.ser.readline() # Read data from serial port
					if data.startswith('_'):
						msg=String()
						msg.data=data
						rospy.loginfo(msg)
						self.pubRaw.publish(msg)

					else:
						try:	
							dataVec=data[0:-1].split("\t")
							msg=serial_data()
							msg.milliseconds=long(dataVec[0])
							msg.rate=long(dataVec[1])
							msg.data=map(float,dataVec[2:-1])
							
							rospy.loginfo(msg)
							self.pub.publish(msg)
						except ValueError:
							rospy.logerr('PRESSURE CONTROL: data was garbled...ignoring it')

				except serial.serialutil.SerialException:
					rospy.logerr('PRESSURE CONTROL: Serial read error...ignoring it')
					
			self.rate.sleep()


if __name__ == '__main__':
	rospy.init_node('serial_talker_node',anonymous=False)
	node = SerialTalkerNode()
	try:
		if rospy.has_param('object_return'):
			params=rospy.get_param('object_return')
			baud=params['baudrate']
			devname=params['devname']
		
		node.talker()
	except rospy.ROSInterruptException:
		pass
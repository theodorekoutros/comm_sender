#!/usr/bin/env python


#Adapted from:
#https://answers.ros.org/question/159276/read-data-from-serial-port-and-publish-over-a-topic/


import roslib;  # roslib.load_manifest('numpy_tutorials') #not sure why I need this
import rosbag
import rospy
from comm_sender.msg import serial_data
from std_msgs.msg import String
import serial_coms

devname = '/dev/ttyACM0'
baud = 115200


def talker():
	ser = serial_coms.resume(devname,baud)
	serial_coms.initialize(ser)

	pub = rospy.Publisher('/object_return/location', serial_data, queue_size=10)
	pubRaw = rospy.Publisher('/object_return/raw', String, queue_size=10)
	rospy.init_node('talker',anonymous=True)
	while not rospy.is_shutdown():
		if ser.in_waiting: # NO ATTRIBUTE IN WAITING !!!!
			try:
				data= ser.readline() # Read data from serial port
				if data.startswith('_'):
					msg=String()
					msg.data=data
					rospy.loginfo(msg)
					pubRaw.publish(msg)

				else:
					try:	
						dataVec=data[0:-1].split("\t")
						msg=serial_data()
						msg.milliseconds=long(dataVec[0])
						msg.rate=long(dataVec[1])
						msg.data=map(float,dataVec[2:])
						
						rospy.loginfo(msg)
						pub.publish(msg)
					except ValueError:
						rospy.logerr('OBJECT RETURN: data was garbled...ignoring it')

			except serial.serialutil.SerialException:
				rospy.logerr('OBJECT RETURN: Serial read error...ignoring it')
				
		#rospy.sleep(1.0)


if __name__ == '__main__':
	try:
		if rospy.has_param('object_return'):
			params=rospy.get_param('object_return')
			baud=params['baudrate']
			devname=params['devname']
		
		talker()
	except rospy.ROSInterruptException:
		pass
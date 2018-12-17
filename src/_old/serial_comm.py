#!/usr/bin/env python

import serial
import time

import sys, select, termios, tty

#ser = serial.Serial('COM4',baudrate = 9600, timeout = 1)

class SerialCommunicationNode:
    def __init__(self):
    	self.node_name = rospy.get_name()
        
        rospy.loginfo("[%s] Initialzing." %(self.node_name))
        
        #self.smthg = SOMETHINGELSE

        #publisher and subscribers
        self.pub_chatter = rospy.Publisher('~chatter', String, queue_size=10)
        
        #self.sub_SOEMTHING = rospy.Subscriber("~SOMETHING", TYPE, self.CALLBACKMETHOD, queue_size=1)
		
		self.rate = rospy.Rate(10) # 10hz        

    def talker(self):
    	# the looper
	    while not rospy.is_shutdown():
	        self.hello_str = "hello world %s" % rospy.get_time()
	        rospy.loginfo(self.hello_str)
	        self.pub_chatter.publish(self.hello_str)
	        #rate.sleep()


	        #self.pub_servo_status = rospy.Publisher("~servo_status", String, queue_size =1)
        	#self.pub_servo_status.publish(String(data="None"))

        	'''
	        settings = termios.tcgetattr(sys.stdin)

			l = getKey()

			if l == SOMETHING : 
			SEND the message to the actual serial as COMMAND + ARGUMENTS

			elif l== SOMETHING else: 
			CHNAGE the messageto be sent 
			etc...
			'''	

	def getKey(self):
	    tty.setraw(sys.stdin.fileno())
	    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
	    if rlist:
	        key = sys.stdin.read(1)
	    else:
	        key = ''

	    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	    return key


if __name__=="__main__":
    rospy.init_node('serial_communication_node', anonymous=False)
    node = SerialCommunicationNode()
    node.talker()
    rospy.spin()





'''
#writing to the serial 
# prefix b is required for Python 3.x, optional for Python 2.x
ser.write(b'5')


def write_in():
		arduinoData = ser.write('1')

def read_from():
		arduinoData = ser.readline().decode('ascii') 

while(1):
	#read from serial

	arduinoData = ser.readline().decode('ascii')
	print(arduinoData)





print("done")



f = open("data.txt", "w")
f.write( str(yEst)  )      # str() converts to string
f.close()




#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
 

'''
import serial
import time

s = serial.Serial('COM15')
s.write('on')

time.sleep(1)

for i in range(1,100):
    line = ser.readline()   # read a '\n' terminated line
    print(line)
    
print("Hello, World!")     # natch
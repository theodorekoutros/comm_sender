#!/usr/bin/env python

import serial

def resume(devname,baud):
	"""Start serial communication
	INPUTS:
		devname - the short name of the device you want to use
		baud    - baud rate
	OUTPUTS:
		s - the serial object created
	"""	
	s = serial.Serial(devname, baud)
	if not s.isOpen():
		s.open()
		
	return s

def initialize(s):
	s.flushInput()  # Flush startup text in serial input
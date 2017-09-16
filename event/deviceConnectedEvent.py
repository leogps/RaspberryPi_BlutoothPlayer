#!/usr/bin/python
# 
#  Author: leogps
#

class DeviceConnectedEvent():

	def __init__(self, mPlayer):
		print "Event Device Connected."
		self.mPlayer = mPlayer

	def getMessage():
		return "Device Connected."
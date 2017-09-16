#!/usr/bin/python
# 
#  Author: leogps
#

"""
	Bluetooth Device class.
"""

__author__ = 'leogps'


from utils import playerutils


class Device:

	def __init__(self, backingDevice):
		self.backingDevice = backingDevice
		propertiesObj = playerutils.retrieveProperties(backingDevice)
		print propertiesObj

	def printProperties(self):
		print "parsing properties... "
		print self.properties
		for prop in self.properties:
			print prop
			print self.properties[prop]

	def getAllProperties(self):
		self.properties = propertiesObj.GetAll("org.bluez.Device1")	
		self.printProperties()
		return self.properties

	def connect(self):
		if(self.backingDevice != None):
			self.backingDevice.Connect()
		else:
			raise

	def pair(self):
		if(self.backingDevice != None):
			self.backingDevice.Pair()
		else:
			raise



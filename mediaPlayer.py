#!/usr/bin/python
# 
#  Author: leogps
#


"""
	Bluetooth MediaPlayer class.
"""

__author__ = 'leogps'

import dbus
from utils import playerutils

class MediaPlayer:

	def __init__(self, backingObject):
		self.backingObject = backingObject

	def getBackingObject(self):
		return self.backingObject		

	def getAllProperties(self):
		propertiesObj = playerutils.retrieveProperties(self.backingObject)
		self.properties = propertiesObj.GetAll("org.bluez.MediaPlayer1")
		#print self.properties
		return self.properties

	def play(self):
		if(self.backingObject != None):
			self.backingObject.Play()
		else:
			raise

	def next(self):
		if(self.backingObject != None):
			self.backingObject.Next()
		else:
			raise			

	def previous(self):
		if(self.backingObject != None):
			self.backingObject.Previous()
		else:
			raise				

	def pause(self):
			if(self.backingObject != None):
				self.backingObject.Pause()
			else:
				raise

	def stop(self):
		if(self.backingObject != None):
			self.backingObject.Stop()
		else:
			raise

	def getProperty(self, propertyKey):
		self.getAllProperties()
		if(self.properties != None):
			return self.properties[propertyKey]
		else:
			raise
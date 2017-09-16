#!/usr/bin/python
# 
#  Author: leogps
#

"""
	Bluetooth Device Test class.
"""

from bluezPythonApi import device


properties = dict({
	"a" : 1,
	"b" : 2,
	"name" : "hello"
	})

device = device.Device(backingDevice=None, properties=properties)

print device

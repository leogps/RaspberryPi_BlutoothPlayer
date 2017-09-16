#!/usr/bin/python
# 
#  Author: leogps
#

from bluezPythonApi.utils import playerutils
import dbus

"""
	Bluetooth Adapter retriever
"""

ADAPTER_INTERFACE = "org.bluez.Adapter1"


class AdapterRetriever:

	def lookupHCI(self):
		objects = self.listAdapters()
		for path, intefaces in objects.iteritems():
			pathStr = "Path: " + path.__str__()
			if pathStr.startswith("/org/bluez/hci"):
				print "Found HCI path: " + pathStr
				return pathStr
		return None


	def findAdapter(self, desiredPath):
		objects = self.listAdapters()		
		for path, interfaces in objects.iteritems():
			if path == desiredPath:
				for key in interfaces:
					print "key: " + key
					if key == ADAPTER_INTERFACE:
						value = interfaces[key]
						print "Adapter found."
						#if type(value) is dbus.Dictionary:
							#print value["UUID"]
							#printDict(value)
						return dbus.Interface(playerutils.getSystemBus().get_object("org.bluez",  desiredPath), dbus_interface=ADAPTER_INTERFACE)
		print "Adapter NOT found!!"
		return None


	def listAdapters(self):
		bus = playerutils.getSystemBus()
		# om = dbus.Interface(bus.get_object(SERVICE, ADAPTER_OBJECT_PATH), OBJECT_MANAGER_INTERFACE)
		# print om

		# objects = om.GetManagedObjects()
		# for path, interfaces in objects.iteritems():
		# 	if ADAPTER_INTERFACE not in interfaces:
		# 		continue
			
		# 	print(" [ %s ]" % (path))

		# 	print interfaces

		# 	props = interfaces[ADAPTER_INTERFACE]

		# 	for (key, value) in props.items():
		# 		if (key == "Class"):
		# 			print("    %s = 0x%06x" % (key, value))
		# 		else:
		# 			print("    %s = %s" % (key, value))	

		# objects = om.GetManagedObjects()
		# for path, interfaces in objects.iteritems():
		# 	if "org.bluez.Device1" not in interfaces:
		# 		continue
		# 	properties = interfaces["org.bluez.Device1"]
		# 	# if properties["Adapter"] != adapter_path:
		# 	# 	continue;
		# 	print("%s %s" % (properties["Address"], properties["Alias"]))	

		objects = playerutils.getCurrentManagedObjects()
		# for path, interfaces in objects.iteritems():
		# 	print path
		# 	print type(interfaces)
		# 	printDict(interfaces)
		return objects

def printDict(object):
	for key in object:
		print key
		value = object[key]
		if type(value) is dbus.Dictionary:
			printDict(value)
		else:
			print value

#AdapterRetriever().listAdapters()

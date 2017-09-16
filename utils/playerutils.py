#!/usr/bin/python
# 
#  Author: leogps
#


import dbus

SERVICE = "org.bluez"
ROOT_OBJECT_PATH = "/"
OBJECT_MANAGER_INTERFACE = "org.freedesktop.DBus.ObjectManager"

def getSystemBus():
	return dbus.SystemBus()

def retrieveProperties(object):
	if(object != None):
		return dbus.Interface(object, dbus_interface="org.freedesktop.DBus.Properties")
	else:
		return None

def getCurrentManagedObjects():
	bus = getSystemBus()
	objectManager = dbus.Interface(bus.get_object(SERVICE, ROOT_OBJECT_PATH), OBJECT_MANAGER_INTERFACE)
	if objectManager is not None:
		return objectManager.GetManagedObjects()
	else:
		return None
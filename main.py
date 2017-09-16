#!/usr/bin/python
# 
#  Author: leogps
#


import sys
import dbus
from utils import playerutils
from event import deviceConnectedEvent
from event import mediaChangedEvent
from delegate import adapterRetriever
from . import device, mediaPlayer
from dbus.mainloop.glib import DBusGMainLoop 
import glib
from ui import bluetoothPlayerUI
from time import sleep
import gobject
import subprocess
from threading import Thread

import atexit

BLUEZ_BUS = "org.bluez"
BLUEZ_HCI_DEVICE_PATH = "/org/bluez/hci0"
PATH_SEP = "/"
BLUETOOTH_DEVICE_UID = "dev_XX_XX_XX_XX_XX_XX" #Add bluetooth device's MAC Address here.

BLUEZ_DEVICE_IFACE = "org.bluez.Device1"
BLUEZ_MEDIA_CTRL_IFACE = "org.bluez.MediaControl1"
BLUEZ_MEDIA_TRANSPORT_IFACE = "org.bluez.MediaTransport1"
BLUEZ_PLAYER = "player0"

playToggler = True

DBusGMainLoop(set_as_default=True)
bus = playerutils.getSystemBus()

def connectAndPlay():
	print "Attempting to connect..."
	dev = retrieveDevice()
	try:
		dev.pair()
	except Exception, e:
		print "Could not pair: "
		print e	
	dev.connect()

	secureAdapter()

	print "Attempting to play..."
	mPlayer = retrieveMediaPlayer(getPlayerPath())
	mPlayer.play()	

def retrieveDevice():
	devicePath = getDevicePath()
	deviceObj = dbus.Interface(bus.get_object(BLUEZ_BUS,  devicePath),
		dbus_interface=BLUEZ_DEVICE_IFACE)
	dev = device.Device(backingDevice=deviceObj)
	return dev

def doRetrieveMediaPlayer():
	devicePath = getDevicePath()
	mediaCtrlObj = dbus.Interface(bus.get_object(BLUEZ_BUS,  devicePath),
		dbus_interface=BLUEZ_MEDIA_CTRL_IFACE)
	
	propertiesObj = dbus.Interface(mediaCtrlObj, dbus_interface="org.freedesktop.DBus.Properties")
	print "Connected?"
	print propertiesObj.Get("org.bluez.MediaControl1", "Connected")
	print "Player Path?"
	mediaPlayer = propertiesObj.Get("org.bluez.MediaControl1", "Player")
	print mediaPlayer

	return mediaPlayer

def retrieveMediaPlayer(playerPath):

	path = doRetrieveMediaPlayer()

	mediaPlayerObj = dbus.Interface(bus.get_object(BLUEZ_BUS, path),
		dbus_interface='org.bluez.MediaPlayer1')
	mPlayer = mediaPlayer.MediaPlayer(backingObject=mediaPlayerObj)
	return mPlayer
	
def getPlayerPath():
	return getDevicePath() + PATH_SEP + BLUEZ_PLAYER	

def getDevicePath():
	return BLUEZ_HCI_DEVICE_PATH + PATH_SEP + BLUETOOTH_DEVICE_UID

def playerHandler(interface, changed, invalidated, path):
	print "Invoked... printing handler args..."

	print interface
	print changed
	print invalidated
	print path

	print "Printing handler args done."

	## Other bluetooth device events are also getting captured. Filtering by the desired device.
	if getDevicePath() in path and piTft != None:
		mPlayer = retrieveMediaPlayer(path)
		event = mediaChangedEvent.MediaChangedEvent(mPlayer)
		piTft.setMediaPlayer(mPlayer)
		piTft.handlePlayerEvent(event)

def initAdapter():
	adapter = retrieveAdapter()
	adapterProperties = dbus.Interface(adapter, dbus_interface="org.freedesktop.DBus.Properties")

	print "Powered?"
	print adapterProperties.Get("org.bluez.Adapter1", "Powered")

	print "Discoverable?"
	print adapterProperties.Get("org.bluez.Adapter1", "Discoverable")

	print "Pairable?"
	print adapterProperties.Get("org.bluez.Adapter1", "Pairable")

	if adapterProperties.Get("org.bluez.Adapter1", "Powered") == 0:
		adapterProperties.Set("org.bluez.Adapter1", "Powered", True)

	if adapterProperties.Get("org.bluez.Adapter1", "Discoverable") == 0:
		adapterProperties.Set("org.bluez.Adapter1", "Discoverable", True)

	if adapterProperties.Get("org.bluez.Adapter1", "Pairable") == 0:
		adapterProperties.Set("org.bluez.Adapter1", "Pairable", True)

	if adapterProperties.Get("org.bluez.Adapter1", "Discovering") == 0:
		adapter.StartDiscovery()

def retrieveAdapter():
	retriever = adapterRetriever.AdapterRetriever()
	hci = retriever.lookupHCI()

	#print BLUEZ_HCI_DEVICE_PATH
	global BLUEZ_HCI_DEVICE_PATH
	print BLUEZ_HCI_DEVICE_PATH
	if hci != None:
		print "hci_device_path: " + hci
		BLUEZ_HCI_DEVICE_PATH = hci
		
	adapter = retriever.findAdapter(BLUEZ_HCI_DEVICE_PATH)
	return adapter

def secureAdapter():
	print "Securing Adapter..."
	adapter = retrieveAdapter()
	if adapter is not None:
		adapterProperties = dbus.Interface(adapter, dbus_interface="org.freedesktop.DBus.Properties")

		if adapterProperties.Get("org.bluez.Adapter1", "Discoverable") == 1:
			print "Setting discoverable to false..."
			adapterProperties.Set("org.bluez.Adapter1", "Discoverable", False)

		if adapterProperties.Get("org.bluez.Adapter1", "Pairable") == 1:
			print "Setting pairable to false..."
			adapterProperties.Set("org.bluez.Adapter1", "Pairable", False)

		if adapterProperties.Get("org.bluez.Adapter1", "Discovering") == 1:
			print "Disabling discovery..."
			adapter.StopDiscovery()
	print "Securing Adapter done."

@atexit.register
def onexit():
	print "Exit called...."
	subprocess.Popen("/bin/bash /root/bluezPythonApi/restartHelperUI.sh", shell=True)
	print "Started restartHelper process."

def printBanner(): 
	print """
		 _                             _                
		|_) |     _ _|_ _  _ _|_|_    |_) |  _  \/ _  __
		|_) | |_|(/_ |_(_)(_) |_| |   |   | (_| / (/_ | 
	"""
	print """
		                _  _    
		---    |  _  _ (_||_) _ 
		       | (/_(_)__||  _> 
  	"""

if __name__ == "__main__":
	printBanner()

	initAdapter()

	while True:
		try:
			connectAndPlay()
			break
		except Exception, e:
			print "Failed to connect to bluetooth device and play..."
			print e
			sleep(5)	

	global piTft
	mPlayer = retrieveMediaPlayer(getPlayerPath())
	piTft = bluetoothPlayerUI.PiTft(mPlayer)			
	
	try:
				
		#gobject.threads_init()

		piTftThread = Thread(target=bluetoothPlayerUI.PiTft, args=(mPlayer,))
		print "Initializing ui..."	
		piTftThread.start()
		piTftThread.join()

		print "Registering Event Listener..."	
		bus.add_signal_receiver(playerHandler,
			bus_name=BLUEZ_BUS,
			dbus_interface="org.freedesktop.DBus.Properties",
			signal_name="PropertiesChanged",
			path_keyword="path")
		print "Registered Event Listener."	
		
		# schedules first scan of touch events
		glib.timeout_add(20, piTft.scanTouchEvents)

		mainloop = gobject.MainLoop()
		mainloop.run()      
	except KeyboardInterrupt:
			pass
	except Exception as e:
		print e
		print("Unable to run the gobject main loop")      

	print("Shutting down...")
	sys.exit(0)


# def performCommand(command):
# 	if(command == '>'):
# 		mPlayer.next()
# 	elif(command == '<'):
# 		mPlayer.previous()
# 	elif(command == 'P'):
# 		global playToggler	
# 		playToggler = not playToggler
# 		if(playToggler):	
# 			mPlayer.play()
# 		else:
# 			mPlayer.pause()
# 	elif(command == 'S'):
# 		mPlayer.stop()


# def readUserInput():	
# 	while True:
# 		command = raw_input('At your command master: ')	
# 		print command
# 		if(command == 'Q' or command == 'q'):
# 			break		
# 		performCommand(command)


# readUserInput()
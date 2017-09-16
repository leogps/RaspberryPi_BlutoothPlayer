#!/usr/bin/python
# 
#  Author: leogps
#

from ..utils import playerutils

class MediaChangedEvent():

	def __init__(self, mPlayer):
		print "Event Media Changed."
		self.mPlayer = mPlayer

	def getMessage(self):
		msg = "None"
		status = ""
		if self.mPlayer:
			try:
				propertiesObj = self.mPlayer.getAllProperties()	
				print propertiesObj
				if "Status" in propertiesObj:
					status = propertiesObj["Status"].capitalize()							
				if "Track" in propertiesObj:
					track = propertiesObj["Track"]
					print track

					if "Artist" in track:
						msg = track["Artist"]
						msg += " | "
					if "Title" in track:
						msg += track["Title"]
				else:
					msg = "N/A"
			except Exception, e:
				print "Could not retrieve media info."
				print e
				msg = "N/A"
		else:
			msg = "Waiting for media player"
		return status, msg


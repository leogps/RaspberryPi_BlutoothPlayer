#!/usr/bin/python
# 
#  Author: leogps
#

import pygame
from pygame.locals import *
import os
import logging
from time import sleep
import sys
import gobject
from threading import Thread
import glib

import atexit
import subprocess

log_format = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,200,0)

RESTART_TXT = "Restart"
touch_buttons = {RESTART_TXT:[(80, 60),(160,120),GREEN]}

class RestartHelperUI(gobject.Source):

	def __init__(self):
		logger.debug("Constructor called.")
		self.render()

	def render(self):
		logger.debug("initing ui...")

		pygame.init()
		pygame.mouse.set_visible(False)

		self.renderUI()   

		self.registerUIEvents()

		# schedules first scan of touch events
		glib.timeout_add(20, self.scanTouchEvents)

		mainloop = gobject.MainLoop()
		mainloop.run()

	def renderUI(self):
		global lcd
		lcd = pygame.display.set_mode((320, 240))
		lcd.fill(BLACK)
		pygame.display.update()

		font_big = pygame.font.Font(None, 50)

		for k,x in touch_buttons.items():
			t = x[0]
			v = x[1]
			clr = x[2]
			rect_width=160 # 2px less than lcd width
			rect_height=120 # 2px less than lcd height
			pygame.draw.rect(lcd, clr, (t[0], t[1], rect_width, rect_height))
			text_surface = font_big.render('%s'%k, True, WHITE)
			rect = text_surface.get_rect(center=v)
			lcd.blit(text_surface, rect)        

		global font_label

		pygame.display.update()

	def scanTouchEvents(self):
		for event in pygame.event.get():

			if(event.type is MOUSEBUTTONDOWN):
				pos = pygame.mouse.get_pos()                
			elif(event.type is MOUSEBUTTONUP):
				pos = pygame.mouse.get_pos()
				#Find which quarter of the screen we're in
				x,y = pos
				logger.debug(x)
				logger.debug(y)
				logger.debug("***")
				if x > 80 and x < 80 + 160 and y > 60 and y < 60 + 120:
					self.restartAndQuit()

			# re-schedule scan of touch events.
		glib.timeout_add(20, self.scanTouchEvents)

	def restartAndQuit(self):
		sys.exit(0)

	@atexit.register
	def onexit():
		print "Exit called...."
		subprocess.Popen("/bin/bash /root/bluezPythonApi/restart.sh", shell=True)
		print "Started restart process."

	def registerUIEvents(self):
		pygame.event.set_allowed(None)
		pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

RestartHelperUI()
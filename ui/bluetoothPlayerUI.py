# 
#  Author: leogps
#

import pygame
from pygame.locals import *
import os
import logging
from time import sleep
from ..utils import playerutils
import sys
import gobject
from threading import Thread

import glib

#import RPi.GPIO as GPIO
 
#Setup the GPIOs as outputs - only 4 and 17 are available
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(4, GPIO.OUT)
#GPIO.setup(17, GPIO.OUT)

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,200,0)

BLUEZ_BUS = "org.bluez"

playToggler = True

PREVIOUS_TXT = '<<'
NEXT_TXT = '>>'
PLAY_PAUSE_TXT = 'Play'
QUIT_TXT = 'Quit'
 
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
 
MARGIN = 20

# Text{Key} : [(Fill_Rect_Co-ordinates), (Text_Center_Co-ordinates)]
touch_buttons = {PREVIOUS_TXT:[(0,0),(80,60),GREEN], 
    NEXT_TXT:[(160,0),(240,60), GREEN], 
    PLAY_PAUSE_TXT:[(0,120),(80,180), GREEN], 
    QUIT_TXT:[(160,120),(240,180), RED]}


class PiTft(gobject.Source):
    def __init__(self, mPlayer): 
        self.mPlayer = mPlayer

        # bus = playerutils.getSystemBus()
        # logger.debug("Registering Event Listener...")        

        logger.debug("initing ui...")

        pygame.init()
        pygame.mouse.set_visible(False)
        
        self.renderUI()   

        self.registerUIEvents()

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
            rect_width=158 # 2px less than lcd width
            rect_height=118 # 2px less than lcd height
            pygame.draw.rect(lcd, clr, (t[0], t[1], rect_width, rect_height))
            text_surface = font_big.render('%s'%k, True, WHITE)
            rect = text_surface.get_rect(center=v)
            lcd.blit(text_surface, rect)        

        global font_label
        font_label = pygame.font.Font(None, 25)

        self.label = font_label.render('Welcome -leogps', True, WHITE)
        label_rect = self.label.get_rect(center=(160, 220))
        lcd.blit(self.label, label_rect)
        pygame.display.update()


    def setMediaPlayer(self, mPlayer):
        self.mPlayer = mPlayer

    def registerUIEvents(self):
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])

        # while True:           
        #     # Scan touchscreen events
        #     for event in pygame.event.get():
                
        #         if(event.type is MOUSEBUTTONDOWN):
        #             pos = pygame.mouse.get_pos()
        #             print pos
        #         elif(event.type is MOUSEBUTTONUP):
        #             pos = pygame.mouse.get_pos()
        #             print pos
        #             #Find which quarter of the screen we're in
        #             x,y = pos
        #             if y < 120:
        #                 if x < 160:
        #                     self.handlePrevious()
        #                 else:
        #                     self.handleNext()
        #             else:
        #                 if x < 160:
        #                     self.handlePlayPause()
        #                 else:
        #                     self.handleQuit()
        #         sleep(0.1)  


    # def highlightButton(self, pos):        
    #     x,y = pos
    #     if y < 120:
    #         if x < 160:
    #             touch_buttons[PREVIOUS_TXT][2] = RED
    #         else:
    #             touch_buttons[NEXT_TXT][2] = RED
    #     else:
    #         if x < 160:
    #             touch_buttons[PLAY_PAUSE_TXT][2] = RED
    #         else:
    #             touch_buttons[QUIT_TXT][2] = RED
    #     self.renderUI()
    #     self.highlighted = True

    def scanTouchEvents(self):
        for event in pygame.event.get():
            
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                # if self.highlighted is not True:
                #     self.highlightButton(pos)
                #print pos
            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                #print pos
                #Find which quarter of the screen we're in
                x,y = pos
                if y < 120:
                    if x < 160:
                        self.handlePrevious()
                    else:
                        self.handleNext()
                else:
                    if x < 160:
                        self.handlePlayPause()
                    else:
                        self.handleQuit()
            
        # re-schedule scan of touch events.
        glib.timeout_add(20, self.scanTouchEvents)
 
        # self.previous_button = ui.Button(ui.Rect(MARGIN, MARGIN, 130, 90), PREVIOUS_TXT)
        # self.previous_button.on_clicked.connect(self.handlePrevious)
        # self.add_child(self.previous_button)
 
        # self.next_button = ui.Button(ui.Rect(170, MARGIN, 130, 90), NEXT_TXT)
        # self.next_button.on_clicked.connect(self.handleNext)
        # self.add_child(self.next_button)
 
        # self.play_pause_button = ui.Button(ui.Rect(MARGIN, 130, 130, 90), PLAY_PAUSE_TXT)
        # self.play_pause_button.on_clicked.connect(self.handlePlayPause)
        # self.add_child(self.play_pause_button)
 
        # self.quit_button = ui.Button(ui.Rect(170, 130, 130, 90), QUIT_TXT)
        # self.quit_button.on_clicked.connect(self.handleQuit)
        # self.add_child(self.quit_button)
                

    def playerHandler(self, interface, changed, invalidated, path):
        """Handle relevant property change signals"""
        iface = interface[interface.rfind(".") + 1:]
        print("Interface: {}; changed: {}".format(iface, changed))

        eventOccurred = None
        if iface == "Device1":
            if "Connected" in changed:
                eventOccurred = deviceConnectedEvent.DeviceConnectedEvent(mPlayer)
        elif iface == "MediaControl1":
            if "Connected" in changed:
                eventOccurred = deviceConnectedEvent.DeviceConnectedEvent(mPlayer)                
        elif iface == "MediaPlayer1":
            eventOccurred = mediaChangedEvent.MediaChangedEvent(mPlayer)
            if "Track" in changed:
                self.track = changed["Track"]
                self.updateDisplay()
            if "Status" in changed:
                self.status = (changed["Status"])    
        
        self.handlePlayerEvent(eventOccurred)

    def updateDisplay(self):
        if self.mPlayer:
            propertiesObj = self.mPlayer.getAllProperties()
            if "Track" in propertiesObj:
                track = propertiesObj["Track"]
                msg = ""           
                if "Artist" in track:
                    msg = track["Artist"]
                    msg += " | "
                if "Title" in track:
                    msg += track["Title"]
                self.updateStatus(msg)
        else:
            print("Waiting for media player")        

    def handlePrevious(self):
        logger.debug("handling previous")
        self.mPlayer.previous()
        self.updateDisplay()

    def handleNext(self):
        logger.debug("handling next")
        self.mPlayer.next()
        self.updateDisplay()
        
    def handlePlayPause(self):
        logger.debug("handling play/pause")
        global playToggler
        playToggler = not playToggler
        if(playToggler):  
            self.mPlayer.play()
        else:
            self.mPlayer.pause()
        self.updateDisplay()            

    def handleQuit(self):
        logger.debug("handling quit")
        sys.exit(0)

    def handlePlayerEvent(self, event):
        logger.debug("handling player event.")
        if(event != None):
            logger.debug(event.getMessage())

            self.updateStatus(event.getMessage())            
        else:
            logger.debug("Event is empty")
            self.updateStatus("Event is empty")            



    def updateStatus(self, msg):
        top_rect = Rect(0, 2, 320, 20)
        lcd.fill(BLACK, top_rect)
        pygame.display.update()

        top_label = font_label.render(msg[0], True, WHITE)
        top_label_rect = top_label.get_rect(center=(160, 2 + 10))
        lcd.blit(top_label, top_label_rect)
        pygame.display.update()

        bottom_rect = Rect(0, 212, 320, 20)
        lcd.fill(BLACK, bottom_rect)
        pygame.display.update()

        bottom_label_rect = self.label.get_rect(center=(160, 222))
        self.label = font_label.render(msg[1], True, WHITE)        
        lcd.blit(self.label, bottom_label_rect)
        pygame.display.update()
 
    # def gpi_button(self, btn, mbtn):
    #     print btn.text
    #     print self.mPlayer
    #     pos = pygame.mouse.get_pos()
    #     print pos

    #     if btn.text == PREVIOUS_TXT:
    #         self.mPlayer.previous()
    #     elif btn.text == NEXT_TXT:
    #         self.mPlayer.next()
    #     elif btn.text == PLAY_PAUSE_TXT:
    #         global playToggler
    #         playToggler = not playToggler
    #         if(playToggler):  
    #             self.mPlayer.play()
    #         else:
    #             self.mPlayer.pause()
    #     elif btn.text == QUIT_TXT:
    #         sys.exit(0)
    #     sleep(0.1)
         
        # if btn.text == '17 on':
        #     GPIO.output(17, False)
        # elif btn.text == '4 on':
        #     GPIO.output(4, False)
        # elif btn.text == '17 off':
        #     GPIO.output(17, True)
        # elif btn.text == '4 off':
        #     GPIO.output(4, True)
 
# ui.init('Raspberry Pi UI', (320, 240))
# pygame.mouse.set_visible(False)
# ui.scene.push(PiTft())
# ui.run()
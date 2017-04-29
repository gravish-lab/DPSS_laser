import pygame, sys, time
from pygame.locals import *
import Adafruit_MCP4725
import numpy as np

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


# Create a DAC instance.
dac1 = Adafruit_MCP4725.MCP4725(address=0x62)
dac2 = Adafruit_MCP4725.MCP4725(address=0x63)

numbuttons = joystick.get_numbuttons()

interval = 0.01

# Buttons
D_UP = 4
D_DOWN = 6
D_LEFT = 7
D_RIGHT = 5
X_ENABLE = 8
Y_ENABLE = 9
SPEED_DEC = 10
SPEED_ENC = 11
HOME = 12
SET_ORIGIN = 13
ORIGIN_SWITCH = 14


loopQuit = False
while loopQuit == False:

	# test joystick axes
	outstr = ""
        axis = [joystick.get_axis(0), joystick.get_axis(1)]
        
        dac1.set_voltage(np.int(4096/2 + (4096/2)*axis[0]))
        dac2.set_voltage(np.int(4096/2 + (4096/2)*axis[1]))

        outstr = outstr + str(1) + ":" + str(axis[0]) + "|"
        outstr = outstr + str(2) + ":" + str(axis[1]) + "|"
 #       print(outstr)

	# test controller buttons
##	outstr = ""
##	for i in range(0,numbuttons):
##    		button = joystick.get_button(i)
##    		outstr = outstr + str(i) + ":" + str(button) + "|"
#	print(outstr)
    
	for event in pygame.event.get():
                         
                if event.type == pygame.JOYBUTTONDOWN:
                        print("joy button down" + str(event.button))

                        if(event.button == D_UP):
                        # set up move variable
                                
                        if(event.button == D_DOWN):
                        # set down move variable

                        if(event.button == D_RIGHT):
                        # set right move variable
                                
                        if(event.button == D_LEFT):
                        # set left move variable

                        if(event.button == X_ENABLE):
                        
                        if(event.button == Y_ENABLE):

                        if(event.button == SPEED_DEC):

                        if(event.button == SPEED_ENC):

                        if(event.button == HOME):

                        if(event.button == SET_ORIGIN):

                        if(event.button == ORIGIN_SWITCH):
                                
                                
                if event.type == pygame.JOYBUTTONUP:
                	print("joy button up" + str(event.button))
                        if(event.button == D_UP):
                        # set up move variable
                                
                        if(event.button == D_DOWN):
                        # set down move variable

                        if(event.button == D_RIGHT):
                        # set right move variable
                                
                        if(event.button == D_LEFT):
                        # set left move variable



                time.sleep(interval)

pygame.quit()
sys.exit()

import pygame
from pygame.locals import *
import os
from time import sleep
import RPi.GPIO as GPIO

# Geometry
screen_width = 800
screen_height = 480

# Colours
WHITE = (255,255,255)
 
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
 
pygame.init()
pygame.mouse.set_visible(True)


lcd = pygame.display.set_mode((screen_width, screen_height))
lcd.fill((0,0,0))
pygame.display.update()
 
font_big = pygame.font.Font(None, 50)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(lcd, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(lcd, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    lcd.blit(textSurf, textRect)

class indicator

    def __init__(self,msg,x,y,w,h,ic,ac,action=None):
        self.x = x

    pygame.draw.rect(lcd, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    lcd.blit(textSurf, textRect)


indicators = 
 

pygame.display.update()


while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print pos
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            print pos
            #Find which quarter of the screen we're in
            x,y = pos
            if y < 120:
                if x < 160:
            
                else:
            
            else:
                if x < 160:
            
                else:

    pygame.display.update()
    clock.tick(15)
    sleep(0.1)

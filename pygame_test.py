import pygame
from pygame.locals import *
import os
from time import sleep


# Geometry
screen_width = 800
screen_height = 480

small_font_size = 20
large_font_size = 50

# Colours
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

# ras pi touchscreen stuff
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# initialize pygame
pygame.init()
pygame.mouse.set_visible(True)

lcd = pygame.display.set_mode((screen_width, screen_height))
lcd.fill((0,0,0))
pygame.display.update()

# styling
font_big = pygame.font.Font(None, 50)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


# def button(msg,x,y,w,h,ic,ac,action=None):
#     mouse = pygame.mouse.get_pos()
#     click = pygame.mouse.get_pressed()
#     print(click)
#     if x+w > mouse[0] > x and y+h > mouse[1] > y:
#         pygame.draw.rect(lcd, ac,(x,y,w,h))
#
#         if click[0] == 1 and action != None:
#             action()
#     else:
#         pygame.draw.rect(lcd, ic,(x,y,w,h))
#
#     smallText = pygame.font.SysFont("comicsansms",20)
#     textSurf, textRect = text_objects(msg, smallText)
#     textRect.center = ( (x+(w/2)), (y+(h/2)) )
#     lcd.blit(textSurf, textRect)

class button:

    def __init__(self,text,x,y,w,h,bkg_color,txt_color,active_color):
        self.text = text
        self.x = round(x*screen_width)
        self.y = round(y*screen_height)
        self.w = round(w*screen_width)
        self.h = round(h*screen_height)

        self.bkg_color = bkg_color
        self.txt_color = txt_color
        self.active_color = active_color
        self.font = pygame.font.SysFont("comicsansms", large_font_size)

        pygame.draw.rect(lcd, self.bkg_color,(self.x,self.y,self.w,self.h))
        self.textSurf, self.textRect = text_objects(self.text, self.font)
        self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        lcd.blit(self.textSurf, self.textRect)

    def update(self):
        self.textSurf, self.textRect = text_objects(self.text, self.font)
        lcd.blit(self.textSurf, self.textRect)



class indicator:

    def __init__(self,text,x,y,w,h,bkg_color,txt_color):
        self.text = text
        self.x = round(x*screen_width)
        self.y = round(y*screen_height)
        self.w = round(w*screen_width)
        self.h = round(h*screen_height)

        self.bkg_color = bkg_color
        self.txt_color = txt_color
        self.font = pygame.font.SysFont("comicsansms", large_font_size)

        pygame.draw.rect(lcd, self.bkg_color,(self.x,self.y,self.w,self.h))
        pygame.draw.rect(lcd, white, (self.x, self.y, self.w, self.h),1)
        self.textSurf, self.textRect = text_objects(self.text, self.font)
        self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        lcd.blit(self.textSurf, self.textRect)

    def update(self):
        self.textSurf, self.textRect = text_objects(self.text, self.font)
        lcd.blit(self.textSurf, self.textRect)


x_indicator = indicator("X-pos", 0, 0, 6/30, 3/16, (100,100,100), (0,0,0))
y_indicator = indicator("Y-pos", 6/30, 0, 6/30, 3/16, (100,100,100), (0,0,0))
oncam_indicator = indicator("On \r cam", 12/30, 0, 3/30, 3/16, (100,100,100), (0,0,0))
laser_indicator = indicator("Laser \r\n on", 15/30, 0, 3/30, 3/16, (100,100,100), (0,0,0))
x_enable_indicator = indicator("x-enabled", 18/30, 0, 6/30, 3/16, (100,100,100), (0,0,0))
y_enable_indicator = indicator("y-enabled", 24/30, 0, 6/30, 3/16, (100,100,100), (0,0,0))

up_button = button("up", 8/30, 4/16, 3/16, 3/16, (100,100,100), (0,0,0),white)
down_button = button("dwn", 8/30, 10/16, 3/16, 3/16, (100,100,100), (0,0,0),white)
left_button = button("lft", 4/30, 7/16, 3/16, 3/16, (100,100,100), (0,0,0),white)
right_button = button("rgh", 12/30, 7/16, 3/16, 3/16, (100,100,100), (0,0,0),white)

pygame.display.update()


while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print(pos)

    pygame.display.update()
    sleep(0.1)

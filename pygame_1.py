import pygame
from pygame.locals import *
import os
from time import sleep

# Geometry
screen_width = 800
screen_height = 480

# Colours
WHITE = (255, 255, 255)

pygame.init()
pygame.mouse.set_visible(True)

lcd = pygame.display.set_mode((screen_width, screen_height))
lcd.fill((0,0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 50)

touch_buttons = {'17 on': (80, 60), '4 on': (240, 60), '17 off': (80, 180), '4 off': (240, 180)}

for k, v in touch_buttons.items():
    text_surface = font_big.render('%s' % k, True, WHITE)
    rect = text_surface.get_rect(center=v)
    lcd.blit(text_surface, rect)

pygame.display.update()


while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print(pos)
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            print(pos)
            #Find which quarter of the screen we're in
            x,y = pos

    # pygame.display.update()
    sleep(0.1)

import pygame
from styling import *

def text_objects(text, font, font_color):
    textSurface = font.render(text, True, font_color)
    return textSurface, textSurface.get_rect()

from debug import *
from flags import *


class button:

    def __init__(self,text,flag, x,y,w,h,bkg_color,
                 txt_color, active_color, screen,
                 font='inconsolata', fontsize=large_font_size,
                 strformat="%s", toggle_action = None):

        self.flag = flag
        self.text = text
        self.x = round(x*screen_width)
        self.y = round(y*screen_height)
        self.w = round(w*screen_width)
        self.h = round(h*screen_height)
        self.fontsize = fontsize
        self.strformat = strformat
        self.toggle_action = toggle_action
        self.lcd = screen

        self.bkg_color = bkg_color
        self.txt_color = txt_color
        self.active_color = active_color
        self.font = pygame.font.SysFont(font, fontsize, bold=True)

        self.rect = pygame.draw.rect(self.lcd, bkg_color,(self.x,self.y,self.w,self.h), 1)

        self.state = False

        self.update()

    def update(self):

        if self.state == True:
            bkg = self.active_color
        else:
            bkg = self.bkg_color

        pygame.draw.rect(self.lcd, bkg,(self.x,self.y,self.w,self.h))
        pygame.draw.rect(self.lcd, bkg_drkr_color, (self.x, self.y, self.w, self.h), 1)

        display_text = self.strformat % self.text
        text_lines = str.split(display_text, '\\')


        for k, string in enumerate(text_lines):
            textSurf, textRect = text_objects(string, self.font, self.txt_color)
            textRect.center = (
            (self.x + (self.w / 2)), (self.y + (self.h / 2) - (len(text_lines) - 1) * self.fontsize / 2 + k * self.fontsize))
            self.lcd.blit(textSurf, textRect)

        pygame.display.update(self.rect)

class oneshot_button(button):
    def on(self):
        self.state = True
        self.update()

    def off(self):
        self.state = False
        self.update()

    def toggle(self):
        self.state = not self.state
        self.update()


class holdable_button(button):
    def on(self):
        self.state = True
        self.update()


    def off(self):
        self.state = False
        self.update()


    def toggle(self):
        self.state = not self.state
        self.update()



class indicator:

    def __init__(self,text,x,y,w,h,bkg_color,
                 txt_color, screen,
                 font='inconsolata',
                 fontsize=large_font_size, strformat="%s"):
        self.text = text
        self.x = round(x*screen_width)
        self.y = round(y*screen_height)
        self.w = round(w*screen_width)
        self.h = round(h*screen_height)
        self.strformat = strformat
        self.lcd = screen

        self.bkg_color = bkg_color
        self.txt_color = txt_color
        self.font = pygame.font.SysFont(font, fontsize, bold=True)

        self.rect = pygame.draw.rect(self.lcd, bkg_color,(self.x,self.y,self.w,self.h), 1)

        self.state = False

        self.update()

    def update(self):
        display_text = self.strformat % self.text

        if self.state == True:
            bkg = self.txt_color
            txt = self.bkg_color
        else:
            txt = self.txt_color
            bkg = self.bkg_color

        pygame.draw.rect(self.lcd, bkg,(self.x,self.y,self.w,self.h))

        self.textSurf, self.textRect = text_objects(display_text, self.font, txt)
        self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        self.lcd.blit(self.textSurf, self.textRect)
        pygame.display.update(self.rect)


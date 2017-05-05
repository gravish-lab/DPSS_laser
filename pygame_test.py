import pygame
from pygame.locals import *
import os
from time import sleep


# Geometry
screen_width = 800
screen_height = 480

top_bar_height = 2/16

small_font_size = 20
large_font_size = 30

# Colours
bkg_color = (39,40,34)
bkg_drkr_color = (39/2,40/2,34/2)

orchid_color = (249,38,114)
blu_color = (102,217,239)
purp_color = (163,126,242)
grn_color = (162,217,43)
arrow_button_color = (98,249,179)


black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

# ras pi touchscreen stuff
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB')
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# initialize pygame
pygame.init()
pygame.mouse.set_visible(True)

lcd = pygame.display.set_mode((screen_width, screen_height))
lcd.fill(bkg_color)
pygame.display.update()

# styling
font_big = pygame.font.Font(None, 50)

def text_objects(text, font, font_color):
    textSurface = font.render(text, True, font_color)
    return textSurface, textSurface.get_rect()

class button:

    def __init__(self,text,x,y,w,h,bkg_color,txt_color,active_color,
                 font='courier', fontsize=large_font_size):
        self.text = str.split(text, '\\')
        self.x = round(x*screen_width)
        self.y = round(y*screen_height)
        self.w = round(w*screen_width)
        self.h = round(h*screen_height)
        self.fontsize = fontsize

        self.bkg_color = bkg_color
        self.txt_color = txt_color
        self.active_color = active_color
        self.font = pygame.font.SysFont(font, fontsize, bold=True)

        pygame.draw.rect(lcd, self.bkg_color,(self.x,self.y,self.w,self.h))
        pygame.draw.rect(lcd, bkg_drkr_color, (self.x, self.y, self.w, self.h), 1)

        self.format_text()

    def format_text(self):
        for k, string in enumerate(self.text):
            textSurf, textRect = text_objects(string, self.font, self.txt_color)
            textRect.center = (
            (self.x + (self.w / 2)), (self.y + (self.h / 2) - (len(self.text) - 1) * self.fontsize / 2 + k * self.fontsize))
            lcd.blit(textSurf, textRect)

    def update(self):
        self.format_text()


class indicator:

    def __init__(self,text,x,y,w,h,bkg_color,txt_color,
                 font='courier', fontsize=large_font_size):
        self.text = text
        self.x = round(x*screen_width)
        self.y = round(y*screen_height)
        self.w = round(w*screen_width)
        self.h = round(h*screen_height)

        self.bkg_color = bkg_color
        self.txt_color = txt_color
        self.font = pygame.font.SysFont(font, fontsize, bold=True)

        pygame.draw.rect(lcd, self.bkg_color,(self.x,self.y,self.w,self.h))
        # pygame.draw.rect(lcd, bkg_drkr_color, (self.x, self.y, self.w, self.h),1)

        self.textSurf, self.textRect = text_objects(self.text, self.font, self.txt_color)
        self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        lcd.blit(self.textSurf, self.textRect)

    def update(self):
        self.textSurf, self.textRect = text_objects(self.text, self.font)
        lcd.blit(self.textSurf, self.textRect)



# bar indicators
jogspd_indicator = indicator("Jog-spd", 0, 0, 6/30, top_bar_height, bkg_color, orchid_color)
nudgedisp_indicator = indicator("Nudge-disp", 6/30, 0, 6/30, top_bar_height, bkg_color, orchid_color)

x_indicator = indicator("X-pos", 12/30, 0, 6/30, top_bar_height, bkg_color, blu_color)
y_indicator = indicator("Y-pos", 18/30, 0, 6/30, top_bar_height, bkg_color, blu_color)

oncam_indicator = indicator("Cam", 24/30, 0, 3/30, top_bar_height, bkg_color, grn_color)
laser_indicator = indicator("LZR", 27/30, 0, 3/30, top_bar_height, bkg_color, grn_color)

# arrow keys
up_button = button("up", 6/30, 3/16, 5/30, 3.8/16, arrow_button_color, (0,0,0),white)
down_button = button("dwn", 6/30, 11/16, 5/30, 3.8/16, arrow_button_color, (0,0,0),white)
left_button = button("lft", 3/30, 7/16, 5/30, 3.8/16, arrow_button_color, (0,0,0),white)
right_button = button("rgh", 9/30, 7/16, 5/30, 3.8/16, arrow_button_color, (0,0,0),white)

# speed buttons
speed_up_button = button("inc", 0/30, 1.1*top_bar_height, 5/30, 4/16, (100,100,100), (0,0,0),white)
speed_down_button = button("dec", 0/30, (16-1.1*4)/16, 5/30, 4/16, (100,100,100), (0,0,0),white)

# right side buttons
x_enable_button = button("x_enable", 15/30, 1.5*top_bar_height, 7/30, 3.5/16, (100,100,100), purp_color,white)
y_enable_button = button("y_enable", 22.5/30, 1.5*top_bar_height, 7/30, 3.5/16, (100,100,100), purp_color,white)
set_orig_button = button("Set-home", 15/30, 1.5*top_bar_height+4/16, 7/30, 3.5/16, (100,100,100), purp_color,white)
home_button = button("Move-home", 22.5/30, 1.5*top_bar_height+4/16, 7/30, 3.5/16, (100,100,100), purp_color,white)
switch_orig_button = button("Origin\\switch", 15/30, 1.5*top_bar_height+8/16, 7/30, 3.5/16, (100,100,100), purp_color,white)
set_nudge_button = button("Set nudge\\distance", 22.5/30, 1.5*top_bar_height+8/16, 7/30, 3.5/16, (100,100,100), purp_color,white)

pygame.display.update()


while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            print(event.pos)

    # print(pygame.mouse.get_pos())

    pygame.display.update()
    sleep(0.1)

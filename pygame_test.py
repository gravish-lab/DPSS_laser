import pygame
from pygame.locals import *
import os
from time import sleep


# Geometry
screen_width = 800
screen_height = 480

top_bar_height = 2.5/16

small_font_size = 30
large_font_size = 40

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

#CONSTANTS FOR MOVE AND JOYSTICK
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
                 font='inconsolata', fontsize=large_font_size, strformat="%s",
                 toggle_action = None):

        self.text = text
        self.x = round(x*screen_width)
        self.y = round(y*screen_height)
        self.w = round(w*screen_width)
        self.h = round(h*screen_height)
        self.fontsize = fontsize
        self.strformat = strformat
        self.toggle_action = toggle_action

        self.bkg_color = bkg_color
        self.txt_color = txt_color
        self.active_color = active_color
        self.font = pygame.font.SysFont(font, fontsize, bold=True)

        self.rect = pygame.draw.rect(lcd, bkg_color,(self.x,self.y,self.w,self.h), 1)

        self.state = False

        self.update()

    def update(self):

        if self.state == True:
            bkg = self.active_color
        else:
            bkg = self.bkg_color

        pygame.draw.rect(lcd, bkg,(self.x,self.y,self.w,self.h))
        pygame.draw.rect(lcd, bkg_drkr_color, (self.x, self.y, self.w, self.h), 1)

        display_text = self.strformat % self.text
        text_lines = str.split(display_text, '\\')


        for k, string in enumerate(text_lines):
            textSurf, textRect = text_objects(string, self.font, self.txt_color)
            textRect.center = (
            (self.x + (self.w / 2)), (self.y + (self.h / 2) - (len(text_lines) - 1) * self.fontsize / 2 + k * self.fontsize))
            lcd.blit(textSurf, textRect)



    def toggle(self):
        self.state = True
        if self.toggle_action != None:
            self.toggle_action()
        self.update()

        sleep(0.1)

        self.state = False
        self.update()

class indicator:

    def __init__(self,text,x,y,w,h,bkg_color,txt_color,
                 font='inconsolata', fontsize=large_font_size, strformat="%s"):
        self.text = text
        self.x = round(x*screen_width)
        self.y = round(y*screen_height)
        self.w = round(w*screen_width)
        self.h = round(h*screen_height)
        self.strformat = strformat

        self.bkg_color = bkg_color
        self.txt_color = txt_color
        self.font = pygame.font.SysFont(font, fontsize, bold=True)

        self.rect = pygame.draw.rect(lcd, bkg_color,(self.x,self.y,self.w,self.h), 1)

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

        pygame.draw.rect(lcd, bkg,(self.x,self.y,self.w,self.h))

        self.textSurf, self.textRect = text_objects(display_text, self.font, txt)
        self.textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        lcd.blit(self.textSurf, self.textRect)

    def toggle(self):
        self.state = not self.state
        self.update()


# bar indicators
jogspd_indicator = button("10", 0, 0, 7.5/30, top_bar_height, bkg_color,white, orchid_color,
                          strformat="V=%s mm/s")
nudgedisp_indicator = button("11", 7.5/30, 0, 7.5/30, top_bar_height, bkg_color, white, orchid_color,
                             strformat="D=%s mm")

def nudge_toggle_action():
    nudge_state = nudgedisp_indicator.state
    jogspd_indicator.state= not nudge_state
    jogspd_indicator.update()

def jog_toggle_action():
    jog_state = jogspd_indicator.state
    nudgedisp_indicator.state = not jog_state
    nudgedisp_indicator.update()

# nudgedisp_indicator.toggle_action = nudge_toggle_action()
# jogspd_indicator.toggle_action = jog_toggle_action()


x_indicator = indicator("X-pos", 15/30, 0, 7.5/30, top_bar_height, bkg_color, blu_color, strformat="x=%s mm")
y_indicator = indicator("Y-pos", 22.5/30, 0, 7.5/30, top_bar_height, bkg_color, blu_color, strformat="y=%s mm")

oncam_indicator = indicator("NUDGE?", 15.5/30, top_bar_height, 3/30, 1/16, bkg_color, grn_color, fontsize=small_font_size)
laser_indicator = indicator("LAZR", 19.5/30, top_bar_height, 3/30, 1/16, bkg_color, grn_color, fontsize=small_font_size)
shutter_indicator = indicator("SHTR", 23.5/30, top_bar_height, 3/30, 1/16, bkg_color, grn_color, fontsize=small_font_size)
nudge_indicator = indicator("CAM", 26.5/30, top_bar_height, 3/30, 1/16, bkg_color, grn_color, fontsize=small_font_size)


# arrow keys
up_button = button("up", 6/30, 3/16, 5/30, 3.8/16, arrow_button_color, white,white)
down_button = button("dwn", 6/30, 11/16, 5/30, 3.8/16, arrow_button_color, white,white)
left_button = button("lft", 3/30, 7/16, 5/30, 3.8/16, arrow_button_color, white,white)
right_button = button("rgh", 9/30, 7/16, 5/30, 3.8/16, arrow_button_color, white,white)

# speed buttons
speed_up_button = button("+V", 0/30, 1.1*top_bar_height, 5/30, 4/16, (100,100,100), white,white)
speed_down_button = button("-V", 0/30, (16-1.1*4)/16, 5/30, 4/16, (100,100,100), white,white)

# right side buttons
x_enable_button = button("x_enable", 15/30, 1.5*top_bar_height, 7/30, 3.5/16, (100,100,100), purp_color,white)
y_enable_button = button("y_enable", 22.5/30, 1.5*top_bar_height, 7/30, 3.5/16, (100,100,100), purp_color,white)
set_orig_button = button("Set-home", 15/30, 1.5*top_bar_height+4/16, 7/30, 3.5/16, (100,100,100), purp_color,white)
home_button = button("Move-home", 22.5/30, 1.5*top_bar_height+4/16, 7/30, 3.5/16, (100,100,100), purp_color,white)
switch_orig_button = button("Origin\\switch", 15/30, 1.5*top_bar_height+8/16, 7/30, 3.5/16, (100,100,100), purp_color,white)
set_nudge_button = button("Set nudge\\distance", 22.5/30, 1.5*top_bar_height+8/16, 7/30, 3.5/16, (100,100,100), purp_color,white)


move_buttons = [up_button, left_button, right_button, down_button]

button_checks = [x_enable_button, y_enable_button,
                 set_orig_button, home_button,
                 switch_orig_button, set_nudge_button,
                 speed_down_button, speed_up_button,
                 jogspd_indicator, nudgedisp_indicator]

#
# def jog(direction):
#     if direction == D_UP:
#
# def change_speed(up_down):
#
# def x_enable():
#
# def y_enable():
#
# def switch_origin():
#
# def home():
#
# def set_home():
#
# def set_nudge_disp():
#


clock = pygame.time.Clock()


while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = event.pos
            print(pos)

            for button in move_buttons:
                if button.rect.collidepoint(pos):

                    if button is up_button:
                        button.toggle()

                        break

                    if button is down_button:
                        break

                    if button is left_button:
                        break

                    if button is right_button:
                        break



            for button in button_checks:
                if button.rect.collidepoint(pos):
                    button.toggle()

                    # deal with selection of nudge or jog
                    if button is nudgedisp_indicator:
                        print('nudge disp')
                        nudge_state = nudgedisp_indicator.state
                        jogspd_indicator.state = not nudge_state
                        jogspd_indicator.update()
                        break

                    if button is jogspd_indicator:
                        print('jog disp')
                        jog_state = jogspd_indicator.state
                        nudgedisp_indicator.state = not jog_state
                        nudgedisp_indicator.update()
                        break


                    # Home

                    # Set origin

                    # X-enable

                    # Y-enable

                    # Switch origin

                    # Change speed

                    # Set nudge displacement



    # print(pygame.mouse.get_pos())

    pygame.display.update()
    # clock.tick(1)

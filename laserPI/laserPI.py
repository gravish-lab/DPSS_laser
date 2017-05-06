import pygame
from pygame.locals import *
from time import sleep

from buttons import *
from styling import *
from galil_funcs import *

DEBUG = 1

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
NUDGE_SELECT = -2
JOG_SELECT = -1

joy_buttons = [D_UP, D_DOWN, D_LEFT, D_RIGHT, X_ENABLE, Y_ENABLE,
               SPEED_DEC, SPEED_ENC, HOME, SET_ORIGIN, ORIGIN_SWITCH]

# ras pi touchscreen stuff
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB')
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# initialize pygame
pygame.init()
pygame.mouse.set_visible(True)
font_big = pygame.font.Font(None, 50)

lcd = pygame.display.set_mode((screen_width, screen_height))
lcd.fill(bkg_color)
pygame.display.update()

# bar indicators
jogspd_indicator = oneshot_button("10", -1,  0, 0, 7.5/30, top_bar_height, bkg_color,white, orchid_color, lcd,
                          strformat="V=%s mm/s")
nudgedisp_indicator = oneshot_button("11", -2, 7.5/30, 0, 7.5/30, top_bar_height, bkg_color, white, orchid_color, lcd,
                             strformat="D=%s mm")

jogspd_indicator.state = True
jogspd_indicator.update()

x_indicator = indicator("X-pos", 15/30, 0, 7.5/30, top_bar_height, bkg_color, blu_color, lcd, strformat="x=%s mm")
y_indicator = indicator("Y-pos", 22.5/30, 0, 7.5/30, top_bar_height, bkg_color, blu_color, lcd, strformat="y=%s mm")

oncam_indicator = indicator("NUDGE?", 15.5/30, top_bar_height, 3/30, 1/16, bkg_color, grn_color, lcd, fontsize=small_font_size)
laser_indicator = indicator("LAZR", 19.5/30, top_bar_height, 3/30, 1/16, bkg_color, grn_color, lcd, fontsize=small_font_size)
shutter_indicator = indicator("SHTR", 23.5/30, top_bar_height, 3/30, 1/16, bkg_color, grn_color, lcd, fontsize=small_font_size)
nudge_indicator = indicator("CAM", 26.5/30, top_bar_height, 3/30, 1/16, bkg_color, grn_color, lcd, fontsize=small_font_size)

# arrow keys
up_button = holdable_button("up", D_UP,  6/30, 3/16, 5/30, 3.8/16, arrow_button_color, white,white, lcd)
down_button = holdable_button("dwn", D_DOWN, 6/30, 11/16, 5/30, 3.8/16, arrow_button_color, white,white, lcd)
left_button = holdable_button("lft", D_LEFT, 3/30, 7/16, 5/30, 3.8/16, arrow_button_color, white,white, lcd)
right_button = holdable_button("rgh", D_RIGHT, 9/30, 7/16, 5/30, 3.8/16, arrow_button_color, white,white, lcd)

# speed buttons
speed_up_button = oneshot_button("+V", SPEED_ENC, 0/30, 1.1*top_bar_height, 5/30, 4/16, (100,100,100), white,white, lcd)
speed_down_button = oneshot_button("-V", SPEED_DEC, 0/30, (16-1.1*4)/16, 5/30, 4/16, (100,100,100), white,white, lcd)

# right side buttons
x_enable_button = oneshot_button("x_enable", X_ENABLE, 15/30, 1.5*top_bar_height, 7/30, 3.5/16, (100,100,100), purp_color,white, lcd)
y_enable_button = oneshot_button("y_enable", Y_ENABLE, 22.5/30, 1.5*top_bar_height, 7/30, 3.5/16, (100,100,100), purp_color,white, lcd)
set_orig_button = oneshot_button("Set-home", SET_ORIGIN, 15/30, 1.5*top_bar_height+4/16, 7/30, 3.5/16, (100,100,100), purp_color,white, lcd)
home_button = oneshot_button("Move-home", HOME, 22.5/30, 1.5*top_bar_height+4/16, 7/30, 3.5/16, (100,100,100), purp_color,white, lcd)
switch_orig_button = oneshot_button("Origin\\switch", ORIGIN_SWITCH, 15/30, 1.5*top_bar_height+8/16, 7/30, 3.5/16, (100,100,100), purp_color,white, lcd)
set_nudge_button = oneshot_button("Set nudge\\distance", 0, 22.5/30, 1.5*top_bar_height+8/16, 7/30, 3.5/16, (100,100,100), purp_color,white, lcd)


buttons = [x_enable_button, y_enable_button,
                 set_orig_button, home_button,
                 switch_orig_button, set_nudge_button,
                 speed_down_button, speed_up_button,
                 jogspd_indicator, nudgedisp_indicator,
                 up_button, left_button, right_button,
                 down_button]

def wait():
    while True:
        for event in pygame.event.get():
            if (event.type == MOUSEBUTTONUP) or (event.type == JOYBUTTONUP):
                return event

clock = pygame.time.Clock()

while True:
    flag = 0
    curr_button = 0

    print(jog_speeds)

    # Scan touchscreen events
    for event in pygame.event.get():
        print(event)
        if event.type is MOUSEBUTTONDOWN:
            pos = event.pos
            print(pos)
            pygame.event.clear()

            for button in buttons:
                if button.rect.collidepoint(pos):
                    flag = button.flag
                    curr_button = button

        elif event.type is pygame.JOYBUTTONDOWN:
            flag = event.button
            event.clear()

    if DEBUG == 1 and flag != 0:
        print('flag = %d' % flag)

    #### event handling
    # Jogging
    if flag == D_UP:
        if jogspd_indicator.state == True:
            curr_button.on()
            jog(D_UP)
            wait()
            jog_stop()
            curr_button.off()
            print('stop %d' % flag)
        else:
            # g.GCommand('')
            pass

    elif flag == D_DOWN:
        if jogspd_indicator.state == True:
            curr_button.on()
            jog(D_DOWN)
            wait()
            jog_stop()
            curr_button.off()
            print('stop %d' % flag)
        else:
            pass

    elif flag == D_LEFT:
        if jogspd_indicator.state == True:
            curr_button.on()
            jog(D_LEFT)
            wait()
            jog_stop()
            curr_button.off()
            print('stop %d' % flag)
        else:
            pass

    elif flag == D_RIGHT:
        if jogspd_indicator.state == True:
            curr_button.on()
            jog(D_RIGHT)
            wait()
            jog_stop()
            curr_button.off()
            print('stop %d' % flag)
        else:
            pass

    # Home
    elif flag == HOME:
        curr_button.on()
        sleep(0.5)
        curr_button.off()

    # Set origin
    elif flag == ORIGIN_SWITCH:
        curr_button.on()
        sleep(0.5)
        curr_button.off()

    # X-enable
    elif flag == X_ENABLE:
        curr_button.toggle()

    # Y-enable
    elif flag == Y_ENABLE:
        curr_button.toggle()

    # Switch origin
    elif flag == SPEED_DEC:
        curr_button.on()
        sleep(0.5)
        curr_button.off()

    # Change speed
    elif flag == SPEED_ENC:
        curr_button.on()
        sleep(0.5)
        curr_button.off()

    # Set home
    elif flag == SET_ORIGIN:
        curr_button.on()
        sleep(0.5)
        curr_button.off()

    # nudge and jog
    elif flag == NUDGE_SELECT:
        curr_button.on()
        print('nudge disp')
        nudge_state = nudgedisp_indicator.state
        jogspd_indicator.state = not nudge_state
        jogspd_indicator.update()

    elif flag == JOG_SELECT:
        curr_button.on()
        print('jog disp')
        jog_state = jogspd_indicator.state
        nudgedisp_indicator.state = not jog_state
        nudgedisp_indicator.update()


    # elif button is set_nudge_button:
    #         # set the nudge
    #         break

    pygame.display.update()
    # clock.tick(1)

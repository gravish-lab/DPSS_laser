
import pygame
from pygame.locals import *
from time import sleep

import pygame_textinput

from debug import *
from flags import *

from buttons import *
from styling import *
from galil_funcs import *

import time

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

jog_speed = jog_speeds()


# initialize joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# bar indicators
jogspd_indicator = oneshot_button(str(jog_speed.speed), -1,  0, 0, 7.5/30, top_bar_height, bkg_color,white, orchid_color, lcd,
                          strformat="V=%s mm/s")
nudgedisp_indicator = oneshot_button("0", -2, 7.5/30, 0, 7.5/30, top_bar_height, bkg_color, white, orchid_color, lcd,
                             strformat="D=%s mm")

jogspd_indicator.state = True
jogspd_indicator.update()

x_indicator = indicator("X-pos", 15.1/30, 0, 7.5/30, top_bar_height, bkg_color, blu_color, lcd, strformat="x=%s mm")
y_indicator = indicator("Y-pos", 22.5/30, 0, 7.5/30, top_bar_height, bkg_color, blu_color, lcd, strformat="y=%s mm")

nudge_indicator = indicator("NUDGE", 15.5/30, top_bar_height*1.3, 3/30, 1/16, bkg_color, grn_color, lcd, fontsize=small_font_size)
laser_indicator = indicator("LAZER ON", 19.5/30, top_bar_height*1.3, 3/30, 1/16, bkg_color, grn_color, lcd, fontsize=small_font_size)
shutter_indicator = indicator("SHUTTER", 23.5/30, top_bar_height*1.3, 3/30, 1/16, bkg_color, grn_color, lcd, fontsize=small_font_size)
oncam_indicator = indicator("ON CAM", 26.5/30, top_bar_height*1.3, 3/30, 1/16, bkg_color, grn_color, lcd, fontsize=small_font_size)

# arrow keys
up_button = holdable_button("up", D_UP,  6.01/30, 3.01/16, 5.01/30, 3.8/16, arrow_button_color, white,white, lcd)
down_button = holdable_button("dwn", D_DOWN, 6.01/30, 11.01/16, 5.01/30, 3.8/16, arrow_button_color, white,white, lcd)
left_button = holdable_button("lft", D_LEFT, 3.01/30, 7.01/16, 5.01/30, 3.8/16, arrow_button_color, white,white, lcd)
right_button = holdable_button("rgh", D_RIGHT, 9.01/30, 7.01/16, 5.01/30, 3.8/16, arrow_button_color, white,white, lcd)

# speed buttons
speed_up_button = oneshot_button("+V", SPEED_ENC, 0/30, 1.1*top_bar_height, 5.01/30, 4.01/16, (100,100,100), white,white, lcd)
speed_down_button = oneshot_button("-V", SPEED_DEC, 0/30, (16-1.1*4)/16, 5.01/30, 4.01/16, (100,100,100), white,white, lcd)

# right side buttons
x_enable_button = oneshot_button("x_enable", X_ENABLE, 15.01/30, 1.5*top_bar_height, 7.01/30, 3.5/16, (100,100,100), purp_color,white, lcd)
y_enable_button = oneshot_button("y_enable", Y_ENABLE, 22.501/30, 1.5*top_bar_height, 7.01/30, 3.5/16, (100,100,100), purp_color,white, lcd)
set_orig_button = oneshot_button("Set-home", SET_ORIGIN, 15.01/30, 1.5*top_bar_height+4.01/16, 7.01/30, 3.5/16, (100,100,100), purp_color,white, lcd)
home_button = oneshot_button("Move-home", HOME, 22.501/30, 1.5*top_bar_height+4.01/16, 7.01/30, 3.501/16, (100,100,100), purp_color,white, lcd)
switch_orig_button = oneshot_button("Origin\\switch", ORIGIN_SWITCH, 15.01/30, 1.5*top_bar_height+8.01/16, 7.01/30, 3.501/16, (100,100,100), purp_color,white, lcd)
set_nudge_button = oneshot_button("Set nudge\\distance", NUDGE_DISP, 22.501/30, 1.5*top_bar_height+8.01/16, 7.01/30, 3.501/16, (100,100,100), purp_color,white, lcd)

joy_buttons = [D_UP, D_DOWN, D_LEFT, D_RIGHT, X_ENABLE, Y_ENABLE,
               SPEED_DEC, SPEED_ENC, HOME, SET_ORIGIN, ORIGIN_SWITCH]

buttons = [x_enable_button, y_enable_button,
                 set_orig_button, home_button,
                 switch_orig_button, set_nudge_button,
                 speed_down_button, speed_up_button,
                 jogspd_indicator, nudgedisp_indicator,
                 up_button, left_button, right_button,
                 down_button]

indicators = [oncam_indicator, laser_indicator, shutter_indicator, nudge_indicator, x_indicator, y_indicator]

off_buttons = [set_orig_button, home_button,
                 switch_orig_button, set_nudge_button,
                 speed_down_button, speed_up_button]


class update_xy():
    def __init__(self):
        self.last_time= 0
        (x, y) = get_curr_position()
        self.x = x
        self.y = y
        self.delay = .1
        
    def update(self):
        curr_time = time.time()

        if curr_time - self.delay > self.last_time:
            
            (x, y) = get_curr_position()
            self.x = x
            self.y = y
            self.last_time = curr_time
        
        x_indicator.text = self.x
        x_indicator.update()
        y_indicator.text = self.y
        y_indicator.update()
        
updatexy = update_xy()

def restore():
    lcd.fill(bkg_color)
    pygame.display.update()
    [butt.update() for butt in buttons]
    [ind.update() for ind in indicators]

def wait():
    while True:
        updatexy.update()
        for event in pygame.event.get():
            if (event.type == MOUSEBUTTONUP) or (event.type == JOYBUTTONUP):
                return event

clock = pygame.time.Clock()
textinput = pygame_textinput.TextInput(font_size = 80, font_family = "inconsolata")

def read_text():
    lcd.fill((225, 225, 225))
    while True:
        events = pygame.event.get()
        for event in events:
            print(event)
            if event.type is MOUSEBUTTONDOWN:
                print(textinput.get_text())
                restore()
                return

        if textinput.update(events):
            return textinput.get_text()

        lcd.blit(textinput.get_surface(), (100, screen_height/2))
        pygame.display.update()
        # clock.tick(30)

while True:
    flag = 0
    curr_button = 0
    # [off.off() for off in off_buttons]

    # Scan touchscreen events
    for event in pygame.event.get():
        print(event)
        if event.type is MOUSEBUTTONDOWN:
            pos = event.pos
            print(pos)
            # pygame.event.clear()

            for button in buttons:
                if button.rect.collidepoint(pos):
                    flag = button.flag


        elif event.type is pygame.JOYBUTTONDOWN:
            flag = event.button
            curr_button = 0


    pygame.display.update()


    if DEBUG == 1 and flag != 0:
        print('flag = %d' % flag)

    #### event handling
    # Jogging
    if flag == D_UP:
        if jogspd_indicator.state == True:
            up_button.on()
            jog(D_UP)
            wait()
            jog_stop()
            up_button.off()
            print('stop %d' % flag)
        else:
            up_button.on()
            nudge(D_UP, float(nudgedisp_indicator.text), float(jogspd_indicator.text))
            wait()
            jog_stop()
            up_button.off()
            print('stop %d' % flag)
            pass


    elif flag == D_DOWN:
        if jogspd_indicator.state == True:
            down_button.on()
            jog(D_DOWN)
            wait()
            jog_stop()
            down_button.off()
            print('stop %d' % flag)
        else:
            down_button.on()
            nudge(D_DOWN, float(nudgedisp_indicator.text), float(jogspd_indicator.text))
            wait()
            jog_stop()
            down_button.off()
            print('stop %d' % flag)

    elif flag == D_LEFT:
        if jogspd_indicator.state == True:
            left_button.on()
            jog(D_LEFT)
            wait()
            jog_stop()
            left_button.off()
            print('stop %d' % flag)
        else:
            left_button.on()
            nudge(D_LEFT, float(nudgedisp_indicator.text), float(jogspd_indicator.text))
            wait()
            jog_stop()
            left_button.off()
            print('stop %d' % flag)

    elif flag == D_RIGHT:
        if jogspd_indicator.state == True:
            right_button.on()
            jog(D_RIGHT)
            wait()
            jog_stop()
            right_button.off()
            print('stop %d' % flag)
        else:
            right_button.on()
            nudge(D_RIGHT, float(nudgedisp_indicator.text), float(jogspd_indicator.text))
            wait()
            jog_stop()
            right_button.off()
            print('stop %d' % flag)

    # X-enable
    elif flag == X_ENABLE:
        wait()
        sleep(.1)
        x_enable_button.toggle()

        # Y-enable
    elif flag == Y_ENABLE:
        wait()
        sleep(.1)
        y_enable_button.toggle()

    # Home
    elif flag == HOME:
        home_button.on()
        wait()
        sleep(.1)
        home_button.off()

    # switch origin
    elif flag == ORIGIN_SWITCH:
        switch_orig_button.on()
        wait()
        sleep(.1)
        switch_orig_button.off()

    # decrease speed
    elif flag == SPEED_DEC:
        jog_speed.decrement()
        speed_set(jog_speed.speed)
        jogspd_indicator.text = str(jog_speed.speed)
        jogspd_indicator.update()

        speed_down_button.on()
        wait()
        sleep(.1)
        speed_down_button.off()

    # Change speed
    elif flag == SPEED_ENC:
        jog_speed.increment()
        speed_set(jog_speed.speed)
        jogspd_indicator.text = str(jog_speed.speed)
        jogspd_indicator.update()

        speed_up_button.on()
        wait()
        sleep(.1)
        speed_up_button.off()

    # Set home
    elif flag == SET_ORIGIN:
        set_orig_button.on()
        wait()
        sleep(.1)
        set_orig_button.off()

    # nudge and jog
    elif flag == NUDGE_SELECT:
        nudgedisp_indicator.on()
        print('nudge disp')
        nudge_state = nudgedisp_indicator.state
        jogspd_indicator.state = not nudge_state
        jogspd_indicator.update()

    elif flag == JOG_SELECT:
        jogspd_indicator.on()
        print('jog disp')
        jog_state = jogspd_indicator.state
        nudgedisp_indicator.state = not jog_state
        nudgedisp_indicator.update()

    elif flag == NUDGE_DISP:
            set_nudge_button.on()
            wait()
            sleep(.1)
            nudge_dist = read_text()
            try:
                nudge_dist = float(nudge_dist)
            except:
                nudge_dist = 0
                
            nudgedisp_indicator.text = str(nudge_dist)
            restore()
            set_nudge_button.on()
            print('out')


    updatexy.update()



    # clock.tick(60)

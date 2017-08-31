
import gclib
#def connect():

import random

from debug import *
from flags import *

import time

import numpy as np

GALIL_DEBUG = 1

if GALIL_DEBUG:
    g = gclib.py()
    g.GOpen('192.168.1.40 -d')

speed_calib = 10000 # mm/s to .1 microns/s

class jog_speeds():
    def __init__(self):

        self.curr_index = 0
        self.speeds = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5,
                      3, 2.5, 4, 4.5, 5, 10, 15, 20, 25, 30, 35,
                      40]
        self.speed = self.speeds[self.curr_index]

    def increment(self):
        self.curr_index = min(self.curr_index+1, len(self.speeds)-1)
        self.speed = self.speeds[self.curr_index]

    def decrement(self):
        self.curr_index = max(self.curr_index-1, 0)
        self.speed = self.speeds[self.curr_index]

class nudge_dists():
    def __init__(self):

        self.curr_index = 0
        self.dists = [0.1,0.2,0.3,0.4,0.5]
        self.dists.extend(list(np.linspace(1,100,100)))
        self.dist = self.dists[self.curr_index]

    def increment(self):
        self.curr_index = min(self.curr_index+1, len(self.dists)-1)
        self.dist = self.dists[self.curr_index]

    def decrement(self):
        self.curr_index = max(self.curr_index-1, 0)
        self.dist = self.dists[self.curr_index]



def connect_and_reset():
    g.GOpen('192.168.1.40 -d')
    g.GCommand('RS')
    time.sleep(2)
    g.GProgramDownloadFile('/home/pi/DPSS_laser/DPSSprogram.dmc')
    g.GCommand('XQ#AUTO')
    

def jog(direction):
    if direction == D_UP:
        if GALIL_DEBUG:
            g.GCommand('d_down=1')
        if DEBUG == 1:
            print('up_on')
        return
    if direction == D_DOWN:
        if GALIL_DEBUG:
            g.GCommand('d_up=1')
        if DEBUG == 1:
            print('down_on')
        return
    if direction == D_LEFT:
        if GALIL_DEBUG:
            g.GCommand('d_left=1')
        if DEBUG == 1:
            print('left_on')
        return
    if direction == D_RIGHT:
        if GALIL_DEBUG:
            g.GCommand('d_right=1')
        if DEBUG == 1:
            print('right_on')
        return

def send_stop():
    g.GCommand('ST')
    g.GCommand('SH;JG 0,0;BG XY;XQ#LOOP')        

def jog_stop():
    if GALIL_DEBUG:
        g.GCommand('d_up=0')
        g.GCommand('d_left=0')
        g.GCommand('d_right=0')
        g.GCommand('d_down=0')
    return

def nudge(direction):
    if direction == D_UP:
        if GALIL_DEBUG:
            g.GCommand('ndg_up=1')
        if DEBUG == 1:
            print('up_on')
        return
    if direction == D_DOWN:
        if GALIL_DEBUG:
            g.GCommand('ndg_dwn=1')
        if DEBUG == 1:
            print('down_on')
        return
    if direction == D_LEFT:
        if GALIL_DEBUG:
            g.GCommand('ndg_lft=1')
        if DEBUG == 1:
            print('left_on')
        return
    if direction == D_RIGHT:
        if GALIL_DEBUG:
            g.GCommand('ndg_rt=1')
        if DEBUG == 1:
            print('right_on')
        return
##    nudge_sp = float(nudge_sp*speed_calib)
##    if direction == D_UP:
##        if GALIL_DEBUG:
##            g.GCommand('SP %d,%d; PRY +%d;BG' % (nudge_sp, nudge_disp))
##        if DEBUG == 1:
##            print('up_nudge: SP %d,%d; PRY +%d;BG' % (nudge_sp, nudge_disp))
##        return
##    if direction == D_DOWN:
##        if GALIL_DEBUG:
##            g.GCommand('SP %d,%d; PRY -%d;BG' % (nudge_sp, nudge_disp))
##        if DEBUG == 1:
##            print('down_nudge: SP %d,%d; PRY -%d;BG' % (nudge_sp, nudge_disp))
##        return
##    if direction == D_LEFT:
##        if GALIL_DEBUG:
##            g.GCommand('SP %d,%d; PRX +%d;BG' % (nudge_sp, nudge_disp))
##        if DEBUG == 1:
##            print('left_nudge: SP %d,%d; PRX +%d;BG' % (nudge_sp, nudge_disp))
##        return
##    if direction == D_RIGHT:
##        if GALIL_DEBUG:
##            g.GCommand('SP %d,%d; PRX -%d;BG' % (nudge_sp, nudge_disp))
##        if DEBUG == 1:
##            print('right_nudgeSP %d,%d; PRX -%d;BG' % (nudge_sp, nudge_disp))
##        return
##

def x_enable(up_down):
    if GALIL_DEBUG:
        g.GCommand('x_enable=%d' % up_down)
    return
#
def y_enable(up_down):
    if GALIL_DEBUG:
        g.GCommand('y_enable=%d' % up_down)
    return

def switch_origin():
    if GALIL_DEBUG:
        g.GCommand('b_switch=1')
    return

def home():
    if GALIL_DEBUG:
        g.GCommand('b_home=1')
    return

def set_home():
    if GALIL_DEBUG:
        g.GCommand('b_set=1')
    return

def speed_set(speed):
    if GALIL_DEBUG:
        g.GCommand('jogspd=%d' % float(speed*speed_calib))

def nudge_set(dist):
    if GALIL_DEBUG:
        g.GCommand('ndg_dst=%d' % float(dist*speed_calib))

def get_vals():
    if GALIL_DEBUG:
        vals = g.GCommand('MG oncam, _TPA, _TPB, homex, homey')
    else:
        vals = '1 2 3 4 5'
        
    return vals

def get_curr_position():
    if GALIL_DEBUG:
        homex = float(g.GCommand('homex='))
        homey = float(g.GCommand('homey='))
        currx = float(g.GCommand('currx='))
        curry = float(g.GCommand('curry='))

    else:
        homex = random.randint(0,10000)
        homey = random.randint(0,10000)
        currx = random.randint(0,10000)
        curry = random.randint(0,10000)

    return (currx - homex, curry - homey)

#
# if event.button == SPEED_DEC:
#     speed_select = float(g.GCommand('a3='))
#     speed_select = speed_select - 0.2
#     g.GCommand('a3=' + str(speed_select))
#
# if event.button == SPEED_ENC:
#     speed_select = float(g.GCommand('a3='))
#     speed_select = speed_select + 0.2
#     g.GCommand('a3=' + str(speed_select))
#

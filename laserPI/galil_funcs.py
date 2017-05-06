
# import gclib
#
# g = gclib.py()
#
# def connect():
#     g.GOpen('192.168.1.40 -d')

jog_speeds = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 2.5,
              3, 2.5, 4, 4.5, 5, 10, 15, 20, 25, 30, 35,
              40, 45, 50, 100, 500, 1000, 1500, 2000]

def jog(direction):
    if direction == D_UP:
        # g.GCommand('d_up=1')
        if DEBUG == 1:
            print('up_on')
        return
    if direction == D_DOWN:
        # g.GCommand('d_down=1')
        if DEBUG == 1:
            print('down_on')
        return
    if direction == D_LEFT:
        # g.GCommand('d_left=1')
        if DEBUG == 1:
            print('left_on')
        return
    if direction == D_RIGHT:
        # g.GCommand('d_right=1')
        if DEBUG == 1:
            print('right_on')
        return

def jog_stop():
    # g.GCommand('d_up=0')
    # g.GCommand('d_left=0')
    # g.GCommand('d_right=0')
    # g.GCommand('d_down=0')
    return

def x_enable(up_down):
    g.GCommand('x_enable=1')
    return
#
def y_enable():
    g.GCommand('y_enable=1')
    return

def switch_origin():
    g.GCommand('b_switch=1')
    return

def home():
    g.GCommand('b_home=1')
    return

def set_home():
    g.GCommand('b_set=1')
    return

def set_nudge_disp():
    return

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
